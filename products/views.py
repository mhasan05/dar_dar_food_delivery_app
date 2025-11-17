from .models import Product, Category
from .serializers import ProductSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class AddProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data['vendor'] = request.user
        category_id = data.get('category')
        if 'image' not in request.FILES:
            return Response({"status": "error", "message": "Image is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not category_id:
            return Response({"status": "error", "message": "Category is required."}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.role not in ['VENDOR','ADMIN']:
            return Response({"status": "error", "message": "unauthorized request"}, status=status.HTTP_403_FORBIDDEN)
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"status": "error", "message": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        data['image'] = request.FILES['image']
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save(category=category)
            return Response({
                "status": "success",
                "message": "Product added successfully.",
                "product": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Product creation failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
