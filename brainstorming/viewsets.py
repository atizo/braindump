import random

from brainstorming.models import Brainstorming, Idea, IDEA_COLORS
from brainstorming.notifications import toggle_notification
from brainstorming.permissions import BrainstromPermissions, edit_mode, bs_set_edit_permission, RATED_IDEAS, set_idea
from brainstorming.serializers import BrainstormingSerializer, IdeaSerializer, BrainstormingWatcherSerializer
from brainstorming.user_session import update_bs_history
from django.db.models import Count
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

SESSION_COLOR = 'prj_id_color'


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
        bs_set_edit_permission(self.request, obj.pk)
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

        rated_ideas = request.session.get(RATED_IDEAS, [])
        if idea.pk not in rated_ideas:
            idea.rate()

            # remember idea, so the user can rate it only once
            rated_ideas.append(idea.pk)
        else:
            idea.unrate()
            rated_ideas.remove(idea.pk)

        request.session[RATED_IDEAS] = rated_ideas

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

        brainstorming = obj.brainstorming.pk

        def get_color():
            used_colors = Idea.objects.filter(brainstorming__pk=obj.brainstorming.pk).exclude(color__exact='') \
                .values('color').annotate(count=Count('color')).order_by('count')

            unused_colors = list(set(IDEA_COLORS) - set([c['color'] for c in used_colors]))
            random_color = None
            if len(unused_colors):
                random_color = random.choice(list(unused_colors))

            # if no color left use to one least used
            return random_color or used_colors[0]['color']

        # check if we have a color assigned for the current project
        if SESSION_COLOR in self.request.session:
            if brainstorming in self.request.session[SESSION_COLOR]:
                color = self.request.session[SESSION_COLOR][brainstorming]
            else:
                color = get_color()
                self.request.session[SESSION_COLOR][brainstorming] = color
        else:
            color = get_color()
            self.request.session[SESSION_COLOR] = {obj.brainstorming.pk: color}

        obj.color = color

        self.request.session.modified = True

        return super(IdeaViewSet, self).pre_save(obj)

    def post_save(self, obj, created=False):
        # remember email for next time
        set_idea(self.request, obj.pk)

        return super(IdeaViewSet, self).post_save(obj, created)