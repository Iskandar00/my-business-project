from django.db import models

from apps.users.models import CustomUser


class AdminPayment(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL,  null=True, limit_choices_to={'role': CustomUser.RoleChoices.Admin})

    card_number = models.CharField(max_length=16)
    amount_of_money = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.card_number}"