from brainstorming.viewsets import BrainstormingViewSet, IdeaViewSet
from django.conf.urls import patterns, url, include
from rest_framework import routers


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'brainstormings', BrainstormingViewSet)
router.register(r'brainstormings/(?P<brainstorming_id>.+)/ideas', IdeaViewSet)

urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
