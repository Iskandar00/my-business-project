from django.db import models
from django.conf import settings


class ProductDislike(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={
            'is_active': True,
            'is_deleted': False,
        },
        related_name='dislikes',
    )
    product = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE,
        related_name='dislikes',
        limit_choices_to={
            'is_active': True,
        },
    )

    def clean(self):
        # Remove the like if a dislike is added by the same user
        if self.user and self.product:
            like_obj = self.product.likes.filter(user=self.user).last()
            if like_obj:
                like_obj.delete()
        super().clean()

    def __str__(self):
        return f"{self.pk}"
