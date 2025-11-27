from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404, handler500
from utils.common_function import custom_error
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('account.urls')),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/settings/', include('settings.urls')),
    path('api/v1/wishlist/', include('wishlist.urls')),
    path('api/v1/order/', include('order.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Hook in the custom error handler for 404 and 500 errors
handler404 = custom_error
handler500 = custom_error
