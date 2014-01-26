import logging
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def index(request):
    # find existing brainstomings in the current session

    return render(request, 'index.html', {})