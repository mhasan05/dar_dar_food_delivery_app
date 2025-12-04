from django.urls import path
from .views import *

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('completed/', CompletedOrderListView.as_view(), name='completed-order-list'),
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('vendor/all_pending_orders/', VendorPendingOrderListView.as_view(), name='vendor_all_pending_orders'),
    path('vendor/all_delivered_orders/', VendorDeliveredOrderListView.as_view(), name='vendor_delivered_orders'),
    path('vendor/all_picked_orders/', VendorPickedOrderListView.as_view(), name='vendor_all_picked_orders'),
    path('vendor/all_past_orders/', VendorPastOrderView.as_view(), name='vendor_all_past_orders'),
    path('vendor/accept_order/<int:order_id>/', VendorAcceptOrderView.as_view(), name='vendor_accept_order'),
    path('vendor/cancel_order/<int:order_id>/', VendorCancelOrderView.as_view(), name='vendor_cancel_order'),
    path('vendor/running_order/', VendorRunningOrderListView.as_view(), name='vendor_running_order'),


    path('rider/all_pending_orders/', RiderPendingOrderListView.as_view(), name='rider_all_pending_orders'),
    path('rider/accept_order/<int:order_id>/', RiderAcceptOrder.as_view(), name='accept_order'),
    path('rider/running_order/', RiderRunningOrderListView.as_view(), name='rider_running_order'),
    path('rider/all_delivered_orders/', RiderDeliveredOrderListView.as_view(), name='rider_delivered_orders'),
    
]
