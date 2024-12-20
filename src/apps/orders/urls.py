from django.urls import path

from apps.orders.views import CreateOrderView, OrderListView, AssignOperatorView

urlpatterns = [
    path('', CreateOrderView.as_view(), name='create_order'),
    path('list/', OrderListView.as_view(), name='create_order_list'),

    path('orders/<int:order_id>/assign-operator/', AssignOperatorView.as_view(), name='assign-operator'),

]
