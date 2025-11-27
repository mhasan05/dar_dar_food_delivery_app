from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer
from products.models import Product
from account.models import *

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all orders for the logged-in user
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
class RiderPendingOrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all orders for the logged-in user
        orders = Order.objects.filter(is_rider_assigned=False,status='CONFIRMED')
        serializer = OrderSerializer(orders, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
class RiderRunningOrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Only riders can view running orders
        if request.user.role != "RIDER":
            return Response(
                {"status": "error", "message": "Only riders can view running orders."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            rider = RiderProfile.objects.get(id=request.user.id)
        except RiderProfile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Rider profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Running orders = assigned to rider + not delivered + not cancelled
        running_orders = Order.objects.filter(
            rider=rider,
            status__in=[
                Order.OrderStatus.CONFIRMED,
                Order.OrderStatus.ASSIGNED
            ]
        ).order_by("-created_at")

        running_order_count = running_orders.count()

        serializer = OrderSerializer(running_orders, many=True)

        return Response(
            {"status": "success","running_order_count":running_order_count, "data": serializer.data},
            status=status.HTTP_200_OK
        )

class VendorRunningOrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Only vendors can access this
        if request.user.role != "VENDOR":
            return Response(
                {"status": "error", "message": "Only vendors can view running orders."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get vendor profile
        try:
            vendor = VendorProfile.objects.get(id=request.user.id)
        except VendorProfile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Vendor profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Running orders = orders involving vendor products AND not delivered/cancelled
        running_orders = (
            Order.objects.filter(
                order_items__product__vendor=vendor,
                status__in=[
                    Order.OrderStatus.CONFIRMED,
                    Order.OrderStatus.ASSIGNED,
                ],
            )
            .distinct()
            .order_by("-created_at")
        )

        serializer = OrderSerializer(running_orders, many=True)
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_200_OK
        )



class VendorPendingOrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "VENDOR":
            return Response(
                {"status": "error", "message": "Only vendors can view their orders."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            vendor = VendorProfile.objects.get(id=request.user.id)
        except VendorProfile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Vendor profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Step 1 & 2 & 3: Get all orders that contain products from this vendor and are pending
        orders = (
            Order.objects.filter(
                order_items__product__vendor=vendor,
                status=Order.OrderStatus.PENDING
            )
            .distinct()
            .order_by("-created_at")
        )

        pending_count = orders.count()

        serializer = OrderSerializer(orders, many=True)

        return Response(
            {"status": "success","total_pending_orders":pending_count, "data": serializer.data},
            status=status.HTTP_200_OK
        )


class VendorPickedOrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "VENDOR":
            return Response(
                {"status": "error", "message": "Only vendors can view their orders."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            vendor = VendorProfile.objects.get(id=request.user.id)
        except VendorProfile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Vendor profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Step 1 & 2 & 3: Get all orders that contain products from this vendor and are pending
        orders = (
            Order.objects.filter(
                order_items__product__vendor=vendor,
                status=Order.OrderStatus.ASSIGNED
            )
            .distinct()
            .order_by("-created_at")
        )

        picked_count = orders.count()

        serializer = OrderSerializer(orders, many=True)

        return Response(
            {"status": "success","total_picked_orders":picked_count, "data": serializer.data},
            status=status.HTTP_200_OK
        )

class VendorPastOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "VENDOR":
            return Response(
                {"status": "error", "message": "Only vendors can view their orders."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            vendor = VendorProfile.objects.get(id=request.user.id)
        except VendorProfile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Vendor profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Step 1 & 2 & 3: Get all orders that contain products from this vendor and are delivered
        orders = (
            Order.objects.filter(
                order_items__product__vendor=vendor,
                status=Order.OrderStatus.DELIVERED
            )
            .distinct()
            .order_by("-created_at")
        )

        past_order_count = orders.count()

        serializer = OrderSerializer(orders, many=True)

        return Response(
            {"status": "success","total_past_orders":past_order_count, "data": serializer.data},
            status=status.HTTP_200_OK
        )

class VendorAcceptOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        # Only vendor can accept orders
        if request.user.role != "VENDOR":
            return Response(
                {"status": "error", "message": "Only vendors can accept orders."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            vendor = VendorProfile.objects.get(id=request.user.id)
        except VendorProfile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Vendor profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Find orders that actually belong to this vendor
        try:
            order = Order.objects.filter(
                order_items__product__vendor=vendor
            ).distinct().get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"status": "error", "message": "Order not found for this vendor."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Only pending orders can be accepted
        if order.status != Order.OrderStatus.PENDING:
            return Response(
                {"status": "error", "message": "Order cannot be accepted at this stage."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Change order status to CONFIRMED
        order.status = Order.OrderStatus.CONFIRMED
        order.save()

        serializer = OrderSerializer(order)

        return Response(
            {"status": "success", "message": "Order accepted successfully!", "data": serializer.data},
            status=status.HTTP_200_OK
        )



class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Extract product and quantity data from the request
        product_data = request.data.get('products', [])
        if not product_data:
            return Response({"status": "error", "message": "No products provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the vendor (shop) of the first product in the list
        first_product_id = product_data[0].get('product_id')
        try:
            first_product = Product.objects.get(id=first_product_id)
        except Product.DoesNotExist:
            return Response({"status": "error", "message": f"Product with ID {first_product_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        first_vendor = first_product.vendor  # The vendor of the first product

        # Create order and initialize total_price
        total_price = 0
        order = Order.objects.create(user=request.user, delivery_address=request.data.get('delivery_address'))

        for item in product_data:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)

            # Fetch product and check if it exists
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"status": "error", "message": f"Product with ID {product_id} not found."}, status=status.HTTP_404_NOT_FOUND)

            # Check if all products belong to the same vendor
            if product.vendor != first_vendor:
                return Response({"status": "error", "message": "You can only order products from the same shop in a single order."}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate total price
            price = product.price * quantity
            total_price += price

            # Create OrderItem
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)

        # Update total price of the order
        order.total_price = total_price
        order.save()

        # Return the serialized order data
        serializer = OrderSerializer(order)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)  # Ensure the order belongs to the logged-in user
        except Order.DoesNotExist:
            return Response({"status": "error", "message": "Order not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)  # Ensure the order belongs to the logged-in user
        except Order.DoesNotExist:
            return Response({"status": "error", "message": "Order not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)

        # Update order status
        order.status = request.data.get('status', order.status)
        order.save()
        serializer = OrderSerializer(order, partial=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)  # Ensure the order belongs to the logged-in user
        except Order.DoesNotExist:
            return Response({"status": "error", "message": "Order not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response({"status": "success", "message": "Order deleted successfully."}, status=status.HTTP_200_OK)



class RiderAcceptOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        # Only riders can accept order
        if request.user.role != "RIDER":
            return Response(
                {"status": "error", "message": "Only riders can accept orders."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get rider profile
        try:
            rider = RiderProfile.objects.get(id=request.user.id)
        except RiderProfile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Rider profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Rider must be available
        if not rider.availability_status:
            return Response(
                {"status": "error", "message": "You are not available to take orders."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get order
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"status": "error", "message": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Order must be pending
        if order.status != 'CONFIRMED':
            return Response(
                {"status": "error", "message": "Order is already accepted or delivered."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Order should not already have rider
        if order.rider is not None:
            return Response(
                {"status": "error", "message": "This order is already assigned to a rider."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Assign rider
        order.rider = rider
        order.status = 'ASSIGNED'
        order.is_rider_assigned = True
        order.save()

        # Make rider busy
        rider.availability_status = False
        rider.save(update_fields=["availability_status"])

        serializer = OrderSerializer(order)

        return Response(
            {"status": "success", "message": "Order accepted successfully!", "data": serializer.data},
            status=status.HTTP_200_OK
        )
