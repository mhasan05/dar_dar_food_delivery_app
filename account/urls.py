from django.urls import path
from account.views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),


    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),



    path('user_profile/', UserProfileView.as_view(), name='user_profile'),
    path('single_user_profile/<int:pk>/', UserProfileView.as_view(), name='single_user_profile'),
    path('update_profile/', UpdateUserProfile.as_view(), name='update_profile'),
    path('update_profile/<int:pk>/', UpdateUserProfile.as_view(), name='update_profile'),
    path('all_users/', AllUserListView.as_view(), name='all_users'),
    path('delete_user/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),


    path('all_shop/', AllShopListView.as_view(), name='all_shop'),
    path('shop/search/', SearchShopView.as_view(), name='search-shop'),

    path('all_grocery/', AllGroceryShopListView.as_view(), name='all_grocery'),



    path('banners/', BannerListCreateView.as_view(), name='banner-list-create'),
    path('banners/<int:pk>/', BannerDetailView.as_view(), name='banner-detail'),

    path('banners/vendor/<int:pk>/', VendorBannerDetailView.as_view(), name='banner-detail'),
]
