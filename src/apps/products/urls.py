from django.urls import path

from apps.products.views import ProductListAPIView


urlpatterns = [
    path('', ProductListAPIView.as_view(), name='payment-list-create'),
]
