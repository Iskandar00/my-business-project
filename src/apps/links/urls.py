from django.urls import path
from apps.links import views

urlpatterns = [
    path('', views.LinkCreateView.as_view(), name='create-link'),
    path('list/', views.ViewLinksAPIView.as_view(), name='list-link')
]
