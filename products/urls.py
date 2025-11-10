from django.urls import path
from account.views import *

urlpatterns = [
    path('product/', UpdateUserProfile.as_view(), name='product'),
]
