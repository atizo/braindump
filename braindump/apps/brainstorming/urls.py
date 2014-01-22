from apps.brainstorming.viewsets import BrainstormingViewSet, IdeaViewSet
from django.conf.urls import patterns, url, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'brainstormings', BrainstormingViewSet)
router.register(r'ideas', IdeaViewSet)

urlpatterns = patterns('braindump.apps.brainstorming.views',
    url(r'^api/', include(router.urls)),
)
