from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Comment(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={
            'is_active': True,
            'is_deleted': False,
        },
        related_name='comments'
    )

    product = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE,
        limit_choices_to={
            'is_active': True
        },
        related_name='comments'
    )

    message = models.CharField(max_length=500)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message}"
