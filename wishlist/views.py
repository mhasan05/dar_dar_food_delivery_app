from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from .serializers import WishlistSerializer
from products.models import Product


class WishlistListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch all wishlist items for the logged-in user
        wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlists, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class AddToWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"status": "error", "message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the product is already in the wishlist
        if Wishlist.objects.filter(user=request.user, product=product).exists():
            return Response({"status": "error", "message": "Product already in your wishlist."}, status=status.HTTP_400_BAD_REQUEST)

        # Add product to the wishlist
        wishlist = Wishlist.objects.create(user=request.user, product=product)
        serializer = WishlistSerializer(wishlist)
        return Response({"status": "success", "message": "Product added to wishlist.", "data": serializer.data}, status=status.HTTP_201_CREATED)


class RemoveFromWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        # Fetch the wishlist item by ID
        try:
            wishlist = Wishlist.objects.get(id=pk, user=request.user)
        except Wishlist.DoesNotExist:
            return Response({"status": "error", "message": "Wishlist item not found or you are not the owner."}, status=status.HTTP_404_NOT_FOUND)

        # Remove the product from the wishlist
        wishlist.delete()
        return Response({"status": "success", "message": "Product removed from wishlist."}, status=status.HTTP_200_OK)
