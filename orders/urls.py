
from django.urls import path
from .views import (OrderListCreateView,OrderDetailView,CartView,CartItemCreateView,CartItemDetailView,)


urlpatterns = [
    # Orders
    path('', OrderListCreateView.as_view(), name='order-list-create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    # Cart
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/items/', CartItemCreateView.as_view(), name='cart-item-create'),
    path('cart/items/<int:pk>/', CartItemDetailView.as_view(), name='cart-item-detail'),
]