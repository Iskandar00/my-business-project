from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.db import models

from apps.users.managers import CustomUserManager


class CustomUser(AbstractUser):
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["fullname"]

    objects = CustomUserManager()
    username = models.CharField(max_length=13, unique=True)
    class RoleChoices(models.TextChoices):
        Director = 'director'
        Admin = 'admin'
        Deliverer = 'deliverer'
        Operator = 'operator'

    role = models.CharField(max_length=10, choices=RoleChoices.choices)

    fullname = models.CharField(max_length=150)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)


    phone_number = models.CharField(max_length=13, unique=True, validators=[
        RegexValidator(
            regex=r"^\+998\d{9}$",
            message="Example: +998 XXXXXXXXX",
            code="uzb_phone_number_validation",
        )
    ])
    email = models.EmailField(_("email address"), blank=True, null=True)

    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    number_of_products_sold = models.PositiveSmallIntegerField(default=0)
    number_of_products_delivered = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.username = self.phone_number
        super().save(*args, **kwargs)

    def __str__(self):
        return self.fullname
