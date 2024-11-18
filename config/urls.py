from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .yasg import *

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(), name='login'),
]

urlpatterns += [
    path('like/', include('apps.likes.urls')),
    path('orders/', include('apps.orders.urls')),
    path('links/', include('apps.links.urls')),
    path('comments/', include('apps.comments.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
