from django.urls import path

from apps.comments import views

urlpatterns = [
    path('create/', views.CommentCreateAPIView.as_view(), name='comment-create'),
    path('list/<int:product_id>', views.CommentListAPIView.as_view(), name='comment-list'),
]