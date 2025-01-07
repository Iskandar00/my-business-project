from django.urls import path
from .views import ProductDeliveryListCreateView, ProductDeliveryRetrieveUpdateDestroyView

urlpatterns = [
    path('', ProductDeliveryListCreateView.as_view(), name='product-delivery-list-create'),
    path('<int:pk>/', ProductDeliveryRetrieveUpdateDestroyView.as_view(), name='product-delivery-detail'),
]
