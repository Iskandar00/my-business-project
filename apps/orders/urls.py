from django.urls import path
from .views import CreateOrderView

urlpatterns = [
    path('<int:pk>/', CreateOrderView.as_view(), name='create_order'),
]
