from django.urls import path

from apps.wishlists import views

urlpatterns = [
    path('create/', views.WishlistCreateAPIView.as_view(), name='wishlist_create'),
    path('list/', views.WishlistListAPIView.as_view(), name='wishlist_list'),
]