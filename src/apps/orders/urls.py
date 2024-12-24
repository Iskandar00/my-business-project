from django.urls import path

from apps.orders.views import CreateOrderView, OrderListView, AssignOperatorView, DashboardStatistic


urlpatterns = [
    path('', CreateOrderView.as_view(), name='create_order'),
    path('list/', OrderListView.as_view(), name='order_list'),

    path('create/<int:order_id>/assign-operator/', AssignOperatorView.as_view(), name='assign-operator'),

    path('dashboard/', DashboardStatistic.as_view(), name='dashboard')

]
