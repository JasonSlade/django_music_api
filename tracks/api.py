from rest_framework import viewsets
from .models import Track
from .serializers import TrackSerializer

from rest_framework import generics, mixins
from .models import Track
from .serializers import TrackSerializer

# /api/tracks/  → GET (list) and POST (create)
class TrackList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
  

# /api/tracks/<id>/ → GET, PUT, DELETE
class TrackDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
