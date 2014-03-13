import json
import logging

from braindump.functions import get_object_or_None
from brainstorming.email_verification import get_verified_email
from brainstorming.models import Brainstorming, Idea, BrainstormingWatcher
from brainstorming.permissions import brainstorming_set_edit_perm
from brainstorming.serializers import BrainstormingSerializer, IdeaSerializer
from brainstorming.user_session import update_bs_history, BS_HISTORY_KEY
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.http import Http404
from django.views.decorators.csrf import ensure_csrf_cookie


logger = logging.getLogger(__name__)


def _get_context(request, brainstorming_id=None):
    # copy history pks to append current
    bs_pks = request.session.get(BS_HISTORY_KEY, [])[:]
    if brainstorming_id:
        bs_pks.append(brainstorming_id)
    brainstorming_serializer = BrainstormingSerializer(Brainstorming.objects.filter(pk__in=bs_pks), many=True,
                                                       context={'request': request})
    brainstorming_store = {}
    idea_store = {}

    for bs in brainstorming_serializer.data:
        bid = bs['id']
        brainstorming_store[bid] = bs
        for idea in IdeaSerializer(Idea.objects.filter(brainstorming__pk=bid), many=True,
                                   context={'request': request}).data:
            if bid not in idea_store:
                idea_store[bid] = {}
            idea_store[bid][idea['id']] = idea

    context = {
        'email': request.session.get('email', ''),
        'name': request.session.get('name', ''),
        'brainstormingStore': json.dumps(brainstorming_store, cls=DjangoJSONEncoder),
        'ideaStore': json.dumps(idea_store, cls=DjangoJSONEncoder),
        'recentBrainstormings': json.dumps(request.session.get(BS_HISTORY_KEY, []), cls=DjangoJSONEncoder),
        'errorMsg': '',
        'infoMsg': ''
    }

    return context


def _set_error(context, msg):
    context['errorMsg'] = msg


def _set_info(context, msg):
    context['infoMsg'] = msg


@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html', _get_context(request))


@ensure_csrf_cookie
def brainstorming(request, brainstorming_id):
    if not Brainstorming.objects.filter(pk=brainstorming_id).exists():
        raise Http404

    update_bs_history(request.session, brainstorming_id)

    return render(request, 'index.html', _get_context(request, brainstorming_id))


@ensure_csrf_cookie
def notification(request, brainstorming_id):
    if not Brainstorming.objects.filter(pk=brainstorming_id).exists():
        raise Http404

    update_bs_history(request.session, brainstorming_id)
    context = _get_context(request, brainstorming_id)

    email = None

    try:
        email = get_verified_email(request)
    except ValueError, ve:
        _set_error(context, ve.message)

    if len(context['errorMsg']) == 0 and email:
        watcher = get_object_or_None(BrainstormingWatcher, brainstorming__id=brainstorming_id, email=email)
        if watcher:
            watcher.delete()
            _set_info(context, 'You receive no more notifications')
        else:
            BrainstormingWatcher.objects.create(brainstorming=Brainstorming.objects.get(pk=brainstorming_id),
                                                email=email)
            _set_info(context, 'You now receive notifications')

    return render(request, 'index.html', context)


@ensure_csrf_cookie
def edit(request, brainstorming_id):
    if not Brainstorming.objects.filter(pk=brainstorming_id).exists():
        raise Http404

    update_bs_history(request.session, brainstorming_id)

    try:
        email = get_verified_email(request)
        if email:
            brainstorming_set_edit_perm(request, brainstorming_id)
        context = _get_context(request, brainstorming_id)
    except ValueError, ve:
        context = _get_context(request, brainstorming_id)
        _set_error(context, ve.message)

    return render(request, 'index.html', context)