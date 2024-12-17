from rest_framework import serializers

from apps.categories.models import Category, SubCategory

class SubCategorySerializer(serializers.ModelSerializer):    
    class Meta:
        model = SubCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = "__all__"