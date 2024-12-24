from rest_framework import serializers
from apps.payments.models import AdminPayment

from apps.general.models import General


class AdminPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminPayment
        fields = ['id', 'user', 'card_number', 'amount_of_money', 'created_at']
        read_only_fields = ['created_at', 'user']

    def validate_card_number(self, value):
        if not value.isdigit() or len(value) != 16:
            raise serializers.ValidationError("Card number must be 16 digits.")
        return value

    def validate_amount_of_money(self, value):
        if value < General.minimum_withdrawal_amount:
            raise serializers.ValidationError("Amount of money must be at least 50,000.")
        return value

