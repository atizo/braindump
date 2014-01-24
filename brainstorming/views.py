import logging
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.cache import cache

logger = logging.getLogger(__name__)

@ensure_csrf_cookie
def index(request):
    # find existing brainstomings ind the current session

    cache.set("foo", "bar")
    logger.info("dfgsdfgsdf")
    logger.info(cache.get("foo"))

    send_mail('Subject here', 'Here is the message.', 'braindump@heroku.com',
    ['aeby@atizo.com'], fail_silently=False)

    return render(request, 'index.html', {})