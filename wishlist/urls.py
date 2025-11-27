from django.urls import path
from .views import WishlistListView, AddToWishlistView, RemoveFromWishlistView

urlpatterns = [
    path('', WishlistListView.as_view(), name='wishlist-list'),
    path('add/', AddToWishlistView.as_view(), name='wishlist-add'),
    path('remove/<int:pk>/', RemoveFromWishlistView.as_view(), name='wishlist-remove'),
]
