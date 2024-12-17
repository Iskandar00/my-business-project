from rest_framework.generics import ListAPIView

from apps.categories.models.category import Category
from apps.categories.seriaalizers import CategorySerializer


class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
