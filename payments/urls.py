
from django.urls import path

from .views import (
    DarajaCallbackView,
    InitiatePaymentView,
    PaymentStatusView,
)

urlpatterns = [
    path("initiate/", InitiatePaymentView.as_view(), name="payment-initiate"),
    path("status/<int:pk>/", PaymentStatusView.as_view(), name="payment-status"),
    path("callback/", DarajaCallbackView.as_view(), name="daraja-callback"),
]
