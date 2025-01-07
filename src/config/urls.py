from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .yasg import *

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += [
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/like/', include('apps.likes.urls')),
    path('api/v1/orders/', include('apps.orders.urls')),
    path('api/v1/links/', include('apps.links.urls')),
    path('api/v1/comments/', include('apps.comments.urls')),
    path('api/v1/products/', include('apps.products.urls')),
    path('api/v1/wishlist/', include('apps.wishlists.urls')),
    path('api/v1/category/', include('apps.categories.urls')),
    path('api/v1/payments/', include('apps.payments.urls')),
    path('api/v1/drivers/', include('apps.drivers.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
