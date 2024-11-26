from django.urls import path

from apps.likes.views import ProductLikeListView
from apps.likes.views.like import ProductLikeToggleView
from apps.likes.views.dislike import ProductDislikeToggleView, ProductDislikeListView

urlpatterns = [
    path('', ProductLikeToggleView.as_view(), name='like'),
    path('list/', ProductLikeListView.as_view(), name='like-list'),
    path('dis/', ProductDislikeToggleView.as_view(), name='dislike'),
    path('dis/list',  ProductDislikeListView.as_view(), name='dislike-list')
]