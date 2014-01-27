import logging
from brainstorming.models import Brainstorming
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def index(request):
    # find existing brainstomings in the current session

    return render(request, 'index.html', {})

@ensure_csrf_cookie
def brain(request, brainstorming_id):
    # find existing brainstomings in the current session
    get_object_or_404(Brainstorming, pk=brainstorming_id)
    return render(request, 'index.html', {})