from django.urls import path
from products.views import *

urlpatterns = [
    path('product/', AddProductView.as_view(), name='product'),
]
