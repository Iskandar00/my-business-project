from django.db import models
from django.conf import settings


class ProductLike(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={
            'is_active': True,
            'is_deleted': False,
        },
        related_name='likes',
    )
    product = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE,
        related_name='likes',
        limit_choices_to={'is_active': True},
    )

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.pk}"

    def clean(self):
        if self.user and self.product:
            # Check if there's a dislike by the same user on this product
            dislike_obj = self.product.dislikes.filter(user=self.user).last()
            if dislike_obj:
                dislike_obj.delete()

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
