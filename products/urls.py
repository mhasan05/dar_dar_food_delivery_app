from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', VendorCategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', VendorCategoryDetailUpdateDeleteView.as_view(), name='vendor-category-detail-update-delete'),

    path('subcategories/', VendorSubCategoryListCreateView.as_view(), name='subcategory-list-create'),
    path('subcategories/<int:pk>/', VendorSubCategoryDetailUpdateDeleteView.as_view(), name='vendor-subcategory-detail-update-delete'),
    path('categories/<int:category_id>/subcategories/', VendorCategoryWiseSubCategoryListView.as_view(), name='category-wise-subcategory-list'),

    path('products/', VendorProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', VendorProductListCreateView.as_view(), name='product-list-create'),
    path('single_products/<int:pk>/', VendorProductDetailUpdateDeleteView.as_view(), name='product-detail-update-delete'),

    path('product_details/<int:pk>/', SingleProductView.as_view(), name='product_details'),
    

    path('products/search/', SearchProductView.as_view(), name='search-products'),
    path('categories/<int:category_id>/products/', CategoryWiseProductListView.as_view(), name='category-wise-products'),
    path('subcategories/<int:subcategory_id>/products/', SubCategoryWiseProductListView.as_view(), name='subcategory-wise-products'),




]
