from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from apps.payments.models import AdminPayment
from apps.payments.serializers import AdminPaymentSerializer


class AdminPaymentView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminPaymentSerializer

    def get_queryset(self):
        return AdminPayment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
