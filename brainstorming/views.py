from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def index(request):
    # find existing brainstomings ind the current session

    return render(request, 'index.html', {})