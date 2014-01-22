from brainstorming.models import Brainstorming, Idea
from brainstorming.serializers import BrainstormingSerializer, IdeaSerializer
from rest_framework import viewsets


class BrainstormingViewSet(viewsets.ModelViewSet):
    queryset = Brainstorming.objects.all()
    serializer_class = BrainstormingSerializer


class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
