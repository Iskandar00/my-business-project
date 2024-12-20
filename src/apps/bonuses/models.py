from django.db import models
from apps.users.models import CustomUser


class BonusMoney(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role__in': [CustomUser.RoleChoices.Admin, CustomUser.RoleChoices.Deliverer]}
    )
    bonus_money = models.IntegerField(default=0)
    card_number = models.CharField(max_length=16)

    def __str__(self):
        return str(self.user)
