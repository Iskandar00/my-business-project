from django.core.validators import RegexValidator
from django.db import models

class General(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    logo = models.ImageField(upload_to='general_logo/')
    banner = models.ImageField(upload_to='general_banner/')
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=13, unique=True, validators=[
        RegexValidator(
            regex=r"^\+998\d{9}$",
            message="Example: +998 XXXXXXXXX",
            code="uzb_phone_number_validation",
        )
    ])

    sayt_url = models.URLField(max_length=100)
    telegram_url = models.URLField(max_length=100)
    instagram_url = models.URLField(max_length=100)
    facebook_url = models.URLField(max_length=100)
    youtube_url = models.URLField(max_length=100)

    operator_fee = models.PositiveIntegerField()
    minimum_withdrawal_amount = models.PositiveIntegerField()

    def __str__(self):
        return self.title