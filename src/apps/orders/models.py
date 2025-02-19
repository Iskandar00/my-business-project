from django.core.validators import RegexValidator, MinValueValidator
from django.db import models, transaction
from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.users.models import CustomUser
from apps.general.models import General


class Order(models.Model):
    link = models.ForeignKey('links.Link', on_delete=models.SET_NULL, blank=True, null=True)

    class AreaChoices(models.IntegerChoices):
        TOSHKENT = 1, 'Toshkent'
        QORAQALPOGISTON = 14, 'Qoraqalpogiston'
        QASHQADARYO = 11, 'Qashqadaryo'
        SIRDAYO = 2, 'Sirdaryo'
        JIZZAX = 3, 'Jizzax'
        FARGONA = 5, 'Fargona'
        NAMANGAN = 6, 'Namangan'
        ANDIJON = 7, 'Andijon'
        BUXORO = 8, 'Buxoro'
        XORAZM = 9, 'Xorazm'
        NAVOIY = 10, 'Navoiy'
        SURXONDARYO = 12, 'Surxondaryo'
        SAMARQAND = 13, 'Samarqand'

    class StatusChoices(models.IntegerChoices):
        YANGI = 1, 'YANGI'
        DASTAVKAGA_TAYYOR = 2, 'DASTAVKAGA_TAYYOR'
        YETKAZILMOQDA = 3, 'YETKAZILMOQDA'
        QAYTA_QUNGIROQ = 4, 'QAYTA_QUNGIROQ'
        YETKAZIB_BERILDI = 5, 'YETKAZIB_BERILDI'
        QAYTIB_KELDI = 6, 'QAYTIB_KELDI'

    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.YANGI)
    admin = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='admin_orders',
        limit_choices_to={'role': CustomUser.RoleChoices.Admin.value}
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='product_orders'
    )
    operator = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='operator_orders',
        limit_choices_to={'role': CustomUser.RoleChoices.Operator.value}
    )

    total_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    estimated_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    product_count = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])
    buyer_name = models.CharField(max_length=50)
    phone_number = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(
                regex=r"^\+998\d{9}$",
                message="Example: +998 XXXXXXXXX",
                code="uzb_phone_number_validation"
            )
        ]
    )
    area = models.IntegerField(choices=AreaChoices.choices)
    order_date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.link and not self.product:
            try:
                raise ValidationError({"product": "Either 'link' or 'product' must be provided."})
            except:
                raise serializers.ValidationError({"product": "Either 'link' or 'product' must be provided."})
        if self.operator:
            self.assign_operator(self.operator.id)

    def save(self, *args, **kwargs):
        self.full_clean()
        with transaction.atomic():
            if self.link:
                self._update_admin_balance()
            if self.operator:
                self._update_operator_balance()

            super().save(*args, **kwargs)

    def _update_admin_balance(self):
        self.admin = self.link.user
        self.product = self.link.product

        if not self.id:
            self.estimated_balance = self.product.admin_money * self.product_count
            self.admin.estimated_balance += self.estimated_balance

        if self.status == self.StatusChoices.YETKAZIB_BERILDI:
            self.total_balance += self.product.admin_money * self.product_count
            self.admin.total_balance += self.product.admin_money * self.product_count
            self.admin.estimated_balance -= self.product.admin_money * self.product_count
            self.admin.bonus_money += self.product.admin_bonus_money * self.product_count

        elif self.status == self.StatusChoices.QAYTIB_KELDI:
            self.admin.estimated_balance -= self.product.admin_money * self.product_count

        self.admin.save()

    def _update_operator_balance(self):
        if not self.operator:
            return

        if self.status == self.StatusChoices.YETKAZIB_BERILDI:
            operator_fee = General.objects.last().operator_fee
            self.operator.total_balance += operator_fee

        self.operator.save()

    def assign_operator(self, user_id):
        user = CustomUser.objects.filter(id=user_id).first()
        if not user or user.role != CustomUser.RoleChoices.Operator.value:
            try:
                raise ValidationError({"operator":"The selected user is not a valid operator."})
            except:
                raise serializers.ValidationError({"operator":"The selected user is not a valid operator."})
        self.operator = user

    def __str__(self):
        return f"Order {self.id} for {self.buyer_name} from {self.get_area_display()}"
