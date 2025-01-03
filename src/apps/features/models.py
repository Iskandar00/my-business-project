from django.db import models
from django.core.exceptions import ValidationError


class Feature(models.Model):
    main_category = models.ForeignKey('categories.Category', on_delete=models.PROTECT, blank=True, null=True)
    sub_category = models.ForeignKey('categories.SubCategory', on_delete=models.PROTECT, blank=True, null=True)

    name = models.CharField(max_length=70)
    slug = models.SlugField(max_length=70, unique=True)

    def __str__(self):
        return self.name

    def clean(self):
        if (bool(self.main_category) + bool(self.sub_category)) != 1:
            raise ValidationError('MainCategory yoki SubCategorydan birini tanlang')

    class Meta:
        verbose_name_plural = 'Features'

    def save(self, *args, **kwargs):
        if self.sub_category:
            self.main_category = self.sub_category.category
        super().save(*args, **kwargs)


class FeatureValue(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='feature_values')
    value = models.CharField(max_length=70)
    slug = models.SlugField(max_length=70, unique=True)

    def __str__(self):
        return f'{self.feature}: {self.value}'

    class Meta:
        unique_together = ('feature', 'value')
