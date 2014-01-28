import json
import logging
from brainstorming.models import Brainstorming
from brainstorming.viewsets import BrainstormingViewSet, IdeaViewSet
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def index(request):
    # find existing brainstomings in the current session

    return render(request, 'index.html', {})


@ensure_csrf_cookie
def brainstorming(request, brainstorming_slug):
    # find existing brainstomings in the current session
    brainstorming = get_object_or_404(Brainstorming, pk=brainstorming_slug)

    initial_brainstorming = BrainstormingViewSet.as_view({'get': 'retrieve'})(
        request, pk=brainstorming.pk).data
    initial_ideas = IdeaViewSet.as_view({'get': 'list'})(
        request, brainstorming=brainstorming.pk).data


    context = {
        'initial_brainstorming': json.dumps(initial_brainstorming),
        'initial_ideas': json.dumps(initial_ideas),
    }

    return render(request, 'index.html', context)