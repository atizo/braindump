from brainstorming.viewsets import BrainstormingViewSet, IdeaViewSet
from django.conf.urls import patterns, url, include
from rest_framework_nested.routers import NestedSimpleRouter, SimpleRouter


router = SimpleRouter()
router.register(r'brainstormings', BrainstormingViewSet)

brainstormings_router = NestedSimpleRouter(router,
    r'brainstormings', lookup='brainstorming')
brainstormings_router.register(r'ideas', IdeaViewSet)

urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(brainstormings_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
