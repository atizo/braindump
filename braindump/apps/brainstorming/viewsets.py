from apps.brainstorming.serializers import BrainstormingSerializer, IdeaSerializer
from rest_framework import viewsets


class BrainstormingViewSet(viewsets.ModelViewSet):
    serializer_class = BrainstormingSerializer


class IdeaViewSet(viewsets.ModelViewSet):
    serializer_class = IdeaSerializer
