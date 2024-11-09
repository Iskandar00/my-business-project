from django.urls import path
from apps.links.views import LinkCreateView

urlpatterns = [
    path('', LinkCreateView.as_view(), name='create-link'),
]
