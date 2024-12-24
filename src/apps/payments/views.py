from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AdminPayment
from .serializers import AdminPaymentSerializer
from rest_framework.permissions import IsAuthenticated


class AdminPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = AdminPayment.objects.filter(user=request.user)
        serializer = AdminPaymentSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = AdminPaymentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
