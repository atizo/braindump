from brainstorming.models import Brainstorming, Idea
from brainstorming.notifications import toggle_notification
from brainstorming.permissions import BrainstromPermissions, edit_mode, set_edit_permission
from brainstorming.serializers import BrainstormingSerializer, IdeaSerializer, BrainstormingWatcherSerializer
from brainstorming.user_session import update_bs_history
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action


class BrainstormingViewSet(viewsets.ModelViewSet):
    queryset = Brainstorming.objects.all()
    serializer_class = BrainstormingSerializer
    permission_classes = (BrainstromPermissions, )

    def pre_save(self, obj):
        # store user's ip address
        obj.creator_ip = self.request.META.get('REMOTE_ADDR', None)
        return super(BrainstormingViewSet, self).pre_save(obj)

    def post_save(self, obj, created=False):
        # remember email for next time
        self.request.session['email'] = obj.creator_email
        set_edit_permission(self.request, obj.pk)
        update_bs_history(self.request.session, obj.pk)

        return super(BrainstormingViewSet, self).post_save(obj, created)

    @action()
    def notification(self, request, pk=None):
        brainstorming = self.get_object()
        serializer = BrainstormingWatcherSerializer(data=request.DATA)
        if serializer.is_valid():
            return Response(toggle_notification(brainstorming, serializer.object.email))
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action()
    def edit(self, request, pk=None):
        brainstorming = self.get_object()
        serializer = BrainstormingWatcherSerializer(data=request.DATA)
        if serializer.is_valid():
            return Response(edit_mode(brainstorming, serializer.object.email))
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    paginate_by = None

    def get_queryset(self):
        queryset = super(IdeaViewSet, self).get_queryset()

        # enforce brainstorming id of current url
        brainstorming_id = self.kwargs.get('brainstorming_id', None)
        if brainstorming_id:
            return queryset.filter(brainstorming__id=brainstorming_id)

        return queryset.none()

    @action(methods=['POST'])
    def rate(self, request, brainstorming_id=None, pk=None):
        idea = self.get_object()

        if idea.pk not in request.session.get('rated_ideas', []):
            idea.rate()

            # remember idea, so the user can rate it only once
            if request.session.get('rated_ideas', None) is None:
                request.session['rated_ideas'] = []
            request.session['rated_ideas'].append(idea.pk)

        idea = Idea.objects.get(pk=idea.pk)
        return Response(IdeaSerializer(idea, context={'request': request}).data)

    def create(self, request, *args, **kwargs):
        # read brainstorming id from url
        request.DATA['brainstorming'] = kwargs.get('brainstorming_id', None)
        return super(IdeaViewSet, self).create(request, *args, **kwargs)

    def pre_save(self, obj):
        # remember name for next time
        self.request.session['name'] = obj.creator_name

        # store user's ip address
        obj.creator_ip = self.request.META.get('REMOTE_ADDR', None)

        return super(IdeaViewSet, self).pre_save(obj)
