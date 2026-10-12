
import logging
from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from rentals.models import Rental

from .models import Payment
from .services import initiate_stk_push

logger = logging.getLogger(__name__)


def callback_metadata(callback):
    metadata = callback.get("CallbackMetadata", {}).get("Item", [])
    return {
        item.get("Name"): item.get("Value")
        for item in metadata
        if item.get("Name")
    }


class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_type = request.data.get("payment_type")
        item_id = request.data.get("item_id")
        phone_number = request.data.get("phone_number")

        if payment_type not in ("order", "rental") or not item_id:
            return Response(
                {"detail": "Provide payment_type (order or rental) and item_id."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not phone_number:
            return Response(
                {"detail": "An M-Pesa phone number is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if payment_type == "order":
            target = get_object_or_404(
                Order,
                pk=item_id,
                customer=request.user,
            )
            if target.status != Order.Status.PENDING:
                return Response(
                    {"detail": "Only pending orders can be paid."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            amount = target.total_amount
            target_field = {"order": target}
            reference = f"ORDER{target.pk}"
            description = f"Drawing order {target.pk}"
        else:
            target = get_object_or_404(
                Rental,
                pk=item_id,
                customer=request.user,
            )
            if target.status not in (
                Rental.Status.PENDING,
                Rental.Status.APPROVED,
            ):
                return Response(
                    {"detail": "This rental cannot be paid in its current status."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            amount = target.total_price
            target_field = {"rental": target}
            reference = f"RENTAL{target.pk}"
            description = f"Equipment rental {target.pk}"

        if amount is None or Decimal(str(amount)) < 1:
            return Response(
                {"detail": "The payment amount must be at least KSh 1."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Avoid starting another STK request while one is still pending.
        existing = Payment.objects.filter(
            status__in=[Payment.Status.INITIATED, Payment.Status.PENDING],
            **target_field,
        ).first()

        if existing:
            return Response(
                {
                    "detail": "A payment attempt is already in progress.",
                    "payment_id": existing.pk,
                },
                status=status.HTTP_409_CONFLICT,
            )

        payment = Payment.objects.create(
            customer=request.user,
            amount=amount,
            phone_number=str(phone_number),
            **target_field,
        )

        try:
            result = initiate_stk_push(
                phone_number=phone_number,
                amount=amount,
                account_reference=reference,
                transaction_desc=description,
            )
        except Exception:
            logger.exception("Failed to initiate Daraja STK Push")
            payment.status = Payment.Status.FAILED
            payment.result_description = "Could not initiate M-Pesa payment."
            payment.save(update_fields=[
                "status", "result_description", "updated_at"
            ])
            return Response(
                {"detail": "Could not initiate payment. Please try again."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        payment.merchant_request_id = result.get("MerchantRequestID", "")
        payment.checkout_request_id = result.get("CheckoutRequestID")
        payment.status = Payment.Status.PENDING
        payment.result_description = result.get("CustomerMessage", "")
        payment.save()

        return Response(
            {
                "payment_id": payment.pk,
                "status": payment.status,
                "message": result.get(
                    "CustomerMessage",
                    "Check your phone and complete the M-Pesa prompt.",
                ),
            },
            status=status.HTTP_201_CREATED,
        )


class PaymentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        payment = get_object_or_404(
            Payment,
            pk=pk,
            customer=request.user,
        )
        return Response({
            "payment_id": payment.pk,
            "status": payment.status,
            "amount": str(payment.amount),
            "receipt_number": (
                payment.mpesa_receipt_number
                if payment.status == Payment.Status.SUCCESS
                else None
            ),
            "result_description": payment.result_description,
        })


class DarajaCallbackView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        callback = (
            request.data.get("Body", {})
            .get("stkCallback", {})
        )

        checkout_id = callback.get("CheckoutRequestID")
        result_code = callback.get("ResultCode")

        if not checkout_id or result_code is None:
            logger.warning("Received malformed Daraja callback")
            return Response({"ResultCode": 0, "ResultDesc": "Accepted"})

        with transaction.atomic():
            payment = (
                Payment.objects.select_for_update()
                .filter(checkout_request_id=checkout_id)
                .first()
            )

            # Acknowledge unknown callbacks without exposing payment details.
            if payment is None:
                logger.warning("Callback received for unknown checkout request")
                return Response({"ResultCode": 0, "ResultDesc": "Accepted"})

            # Make duplicate callbacks harmless.
            if payment.status == Payment.Status.SUCCESS:
                return Response({"ResultCode": 0, "ResultDesc": "Accepted"})

            payment.callback_payload = request.data
            payment.result_code = str(result_code)
            payment.result_description = callback.get(
                "ResultDesc", ""
            )

            if str(result_code) != "0":
                payment.status = Payment.Status.FAILED
                payment.save()
                return Response({"ResultCode": 0, "ResultDesc": "Accepted"})

            metadata = callback_metadata(callback)
            receipt = metadata.get("MpesaReceiptNumber")
            received_amount = metadata.get("Amount")

            expected_amount = int(Decimal(payment.amount).quantize(Decimal("1")))

            # Never mark paid if essential transaction details are missing
            # or the callback amount differs from the stored amount.
            if (
                not receipt
                or received_amount is None
                or Decimal(str(received_amount)) != Decimal(expected_amount)
            ):
                payment.status = Payment.Status.FAILED
                payment.result_description = (
                    "Payment callback details could not be verified. "
                    "Contact support if you were charged."
                )
                payment.save()
                logger.error(
                    "Daraja callback verification mismatch for payment %s",
                    payment.pk,
                )
                return Response({"ResultCode": 0, "ResultDesc": "Accepted"})

            payment.mpesa_receipt_number = str(receipt)
            payment.status = Payment.Status.SUCCESS
            payment.save()


            # Only a successful drawing payment changes order status.
            # Rental approval and activation remain separate staff actions.
           # Update drawing order status after successful payment.
            if payment.order_id:
                order = payment.order

                if order.status == Order.Status.PENDING:
                    order.status = Order.Status.PAID
                    order.save(update_fields=["status", "updated_at"])

            # Update rental status after successful payment.
            elif payment.rental_id:
                rental = payment.rental

                if rental.status in (
                    Rental.Status.PENDING,
                    Rental.Status.APPROVED,
                ):
                    rental.status = Rental.Status.PAID
                    rental.save(update_fields=["status", "updated_at"])

        return Response({"ResultCode": 0, "ResultDesc": "Accepted"})
