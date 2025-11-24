from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import *
from .serializers import *
from account.models import *


# ----------------- Category CRUD API -----------------
class VendorCategoryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filter categories by the logged-in vendor
        user = request.user
        role = str(user.role).upper()
        if role == 'VENDOR':
            categories = Category.objects.filter(vendor=user)
        else:
            categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        # Ensure only vendors can create categories
        if request.user.role != 'VENDOR':
            return Response({"status": "error", "message": "You must be a vendor to create categories."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        data['vendor'] = request.user.id  # Assign the logged-in vendor to the category

        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Save the category with the vendor
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class VendorCategoryDetailUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            category = Category.objects.get(id=pk, vendor=request.user)  # Ensure the category belongs to the logged-in vendor
        except Category.DoesNotExist:
            return Response({"status": "error", "message": "Category not found or you are not the owner."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        try:
            category = Category.objects.get(id=pk, vendor=request.user)  # Ensure the category belongs to the logged-in vendor
        except Category.DoesNotExist:
            return Response({"status": "error", "message": "Category not found or you are not the owner."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Save the updated category
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            category = Category.objects.get(id=pk, vendor=request.user)  # Ensure the category belongs to the logged-in vendor
        except Category.DoesNotExist:
            return Response({"status": "error", "message": "Category not found or you are not the owner."}, status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response({"status": "success", "message": "Category deleted successfully."}, status=status.HTTP_200_OK)

# ----------------- SubCategory CRUD API -----------------
class VendorSubCategoryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filter subcategories by the logged-in vendor
        user = request.user
        role = str(user.role).upper()
        if role == 'VENDOR':
            subcategories = SubCategory.objects.filter(vendor=user)
        else:
            subcategories = SubCategory.objects.all()
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        # Ensure only vendors can create subcategories
        if request.user.role != 'VENDOR':
            return Response({"status": "error", "message": "You must be a vendor to create subcategories."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        data['vendor'] = request.user.id  # Assign the logged-in vendor to the subcategory

        serializer = SubCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Save the subcategory with the vendor
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# ----------------- Product CRUD API -----------------
class VendorProductListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,pk=None):
        # Filter products by the logged-in vendor
        if pk:
            user = UserAuth.objects.filter(pk=pk).first()
        else:
            user = request.user
        role = str(user.role).upper()
        if role == 'VENDOR':
            products = Product.objects.filter(vendor=user)
        else:
            products = Product.objects.all()
        products_count = products.count()
        serializer = ProductSerializer(products, many=True)
        return Response({"status": "success", "products_count": products_count, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        # Ensure only vendors can create products
        if request.user.role != 'VENDOR':
            return Response({"status": "error", "message": "You must be a vendor to create products."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        data['vendor'] = request.user.id  # Assign the logged-in vendor to the product

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Save the product with the vendor
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class VendorSubCategoryDetailUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            subcategory = SubCategory.objects.get(id=pk, vendor=request.user)  # Ensure the subcategory belongs to the logged-in vendor
        except SubCategory.DoesNotExist:
            return Response({"status": "error", "message": "SubCategory not found or you are not the owner."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubCategorySerializer(subcategory)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        try:
            subcategory = SubCategory.objects.get(id=pk, vendor=request.user)  # Ensure the subcategory belongs to the logged-in vendor
        except SubCategory.DoesNotExist:
            return Response({"status": "error", "message": "SubCategory not found or you are not the owner."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubCategorySerializer(subcategory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Save the updated subcategory
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            subcategory = SubCategory.objects.get(id=pk, vendor=request.user)  # Ensure the subcategory belongs to the logged-in vendor
        except SubCategory.DoesNotExist:
            return Response({"status": "error", "message": "SubCategory not found or you are not the owner."}, status=status.HTTP_404_NOT_FOUND)

        subcategory.delete()
        return Response({"status": "success", "message": "SubCategory deleted successfully."}, status=status.HTTP_200_OK)

class VendorCategoryWiseSubCategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id):
        # Filter subcategories by the provided category_id
        user = request.user
        role = str(user.role).upper()
        if role == 'VENDOR':
            subcategories = SubCategory.objects.filter(category_id=category_id, vendor=user)
        else:
            subcategories = SubCategory.objects.filter(category_id=category_id)

        if not subcategories:
            return Response({
                "status": "error",
                "message": "No subcategories found for this category."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = SubCategorySerializer(subcategories, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

# ----------------- Product Detail, Update, Delete -----------------
class VendorProductDetailUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk, vendor=request.user)  # Ensure the product belongs to the logged-in vendor
        except Product.DoesNotExist:
            return Response({"status": "error", "message": "Product not found or you are not the owner."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        try:
            product = Product.objects.get(id=pk, vendor=request.user)  # Ensure the product belongs to the logged-in vendor
        except Product.DoesNotExist:
            return Response({"status": "error", "message": "Product not found or you are not the owner."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Save the updated product
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk, vendor=request.user)  # Ensure the product belongs to the logged-in vendor
        except Product.DoesNotExist:
            return Response({"status": "error", "message": "Product not found or you are not the owner."}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({"status": "success", "message": "Product deleted successfully."}, status=status.HTTP_200_OK)



class SearchProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = str(user.role).upper()
        # Get search query parameters
        query = request.GET.get('q', '')
        
        if query:
            # Search products by name or description (case-insensitive)
            if role == 'VENDOR':
                products = Product.objects.filter(
                    name__icontains=query, vendor=user
                ) | Product.objects.filter(
                    description__icontains=query, vendor=user
                )
            else:
                products = Product.objects.filter(
                    name__icontains=query
                ) | Product.objects.filter(
                    description__icontains=query
                )

            if not products.exists():
                return Response({
                    "status": "error",
                    "message": "No products found matching the search query."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductSerializer(products, many=True)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "status": "error",
            "message": "Search query is required."
        }, status=status.HTTP_400_BAD_REQUEST)
    

class CategoryWiseProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id):
        # Filter products by category_id
        user = request.user
        role = str(user.role).upper()
        if role == 'VENDOR':
            products = Product.objects.filter(category_id=category_id, vendor=user)
        else:
            products = Product.objects.filter(category_id=category_id)

        if not products.exists():
            return Response({
                "status": "error",
                "message": "No products found for this category."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(products, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

class SubCategoryWiseProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subcategory_id):
        # Filter products by category_id
        user = request.user
        role = str(user.role).upper()
        if role == 'VENDOR':
            products = Product.objects.filter(subcategory=subcategory_id, vendor=user)
        else:
            products = Product.objects.filter(subcategory=subcategory_id)

        if not products.exists():
            return Response({
                "status": "error",
                "message": "No products found for this category."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(products, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
