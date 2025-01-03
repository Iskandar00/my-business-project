from django.urls import path

from apps.orders import views


urlpatterns = [
    path('', views.CreateOrderView.as_view(), name='create_order'),
    path('operator-orders/', views.OperatorOrdersView.as_view(), name='operator_orders'),
    path('all-orders-with-operator/', views.AllOrdersWithOperatorView.as_view(), name='all_orders_with_operator'),
    path('all-orders/', views.AllOrdersView.as_view(), name='all_orders'),

    path('create/<int:order_id>/assign-operator/', views.AssignOperatorView.as_view(), name='assign-operator'),

    path('dashboard/', views.DashboardStatistic.as_view(), name='dashboard')

]
