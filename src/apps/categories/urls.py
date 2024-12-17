from django.urls import path

from apps.categories import views


urlpatterns = [
    path('list/', views.CategoryListAPIView.as_view(), name="category_list"),
]