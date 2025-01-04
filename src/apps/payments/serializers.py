from rest_framework import serializers
from apps.payments.models import AdminPayment

from apps.general.models import General


class AdminPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminPayment
        fields = ['user', 'card_number', 'amount_of_money', 'created_at']
        read_only_fields = ['created_at', 'user']

    def validate_card_number(self, value):
        if not value.isdigit() or len(value) != 16:
            raise serializers.ValidationError("Card number must be 16 digits.")
        return value

    def validate_amount_of_money(self, value):
        minimum_withdrawal_amount = General.objects.last().minimum_withdrawal_amount
        if value < minimum_withdrawal_amount:
            raise serializers.ValidationError(f"Amount of money must be at least {minimum_withdrawal_amount}.")
        return value
