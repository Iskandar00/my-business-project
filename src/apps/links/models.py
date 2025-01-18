from django.conf import settings
from django.db import models

from rest_framework import serializers

from apps.general.models import General
from apps.general.unique_id import generate_unique_id
from apps.users.models import CustomUser


class Link(models.Model):
    id_generate = models.CharField(
        unique=True,
        max_length=8,
        editable=False,
        default=generate_unique_id
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={
            'is_active': True,
            'is_deleted': False,
            'role': CustomUser.RoleChoices.Admin.value
        },
        related_name='links',
    )
    product = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE,
        related_name='links',
        limit_choices_to={'is_active': True},
    )
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def url_generate(self):
        general = General.objects.first()
        if not general:
            raise serializers.ValidationError("URL generation failed.")
        sayt_url = general.sayt_url
        return f'{sayt_url}api/v1/orders/?link={self.id_generate}'

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

