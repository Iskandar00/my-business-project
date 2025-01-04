from django.urls import path
from apps.payments.views import AdminPaymentView

urlpatterns = [
    path('', AdminPaymentView.as_view(), name='payment-list-create'),
]
