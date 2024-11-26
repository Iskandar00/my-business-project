from django.db import models
from django.conf import settings



class Wishlist(models.Model):

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={
            'is_active': True,
            'is_deleted': False,
        },
        related_name='wishlists',
    )
    product = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE,
        related_name='wishlists',
        limit_choices_to={'is_active': True},
    )

    class Meta:
        db_table = 'wishlist'

    def __str__(self):
        return self.user