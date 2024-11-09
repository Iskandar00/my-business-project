from rest_framework import generics
from apps.links.models import Link
from apps.links.serializers import LinkSerializer


class LinkCreateView(generics.CreateAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

    def perform_create(self, serializer):
        link = serializer.save()
        self.response_data = {
            "id_generate": link.id_generate,
            "url_generate": link.url_generate(),
        }
