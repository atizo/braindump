from urllib import urlencode
from urlparse import parse_qs, urlsplit, urlunsplit

from braindump.env import get_full_url
from braindump.functions import get_object_or_None
from brainstorming.models import EmailVerification
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


CALLBACK_VERIFICATION_PARAM = 'ev'


def set_query_parameter(url, param_name, param_value):
    """Given a URL, set or replace a query parameter and return the
    modified URL.

    >>> set_query_parameter('http://example.com?foo=bar&biz=baz', 'foo', 'stuff')
    'http://example.com?foo=stuff&biz=baz'

    """
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    query_params[param_name] = [param_value]
    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))


def send_email_verification(to, subject, callback, template, context={}):
    """
    Template must include an {{ url }} placeholder
    """
    ev = EmailVerification.objects.create(email=to)
    callback = set_query_parameter(callback, CALLBACK_VERIFICATION_PARAM, ev.id)
    if not callback.startswith('http'):
        callback = get_full_url(callback)
    context['url'] = callback
    send_mail(subject,
              render_to_string(template, context),
              settings.FORM_MAIL,
              [to],
              fail_silently=False)


def get_verified_email(request):
    if CALLBACK_VERIFICATION_PARAM in request.GET:
        ev = get_object_or_None(EmailVerification, pk=request.GET[CALLBACK_VERIFICATION_PARAM])
        if ev:
            ev.delete()
            return ev.email
        else:
            raise ValueError('Invalid verification code')
