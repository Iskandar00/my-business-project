from django.urls import path

from apps.likes.views.like import ProductLikeToggleView
from apps.likes.views.dislike import ProductDislikeToggleView

urlpatterns = [
    path('', ProductLikeToggleView.as_view(), name='like'),
    path('dis/', ProductDislikeToggleView.as_view(), name='dislike')
]