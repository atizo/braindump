import json
import logging
from braindump.functions import get_object_or_None
from brainstorming.email_verification import get_verified_email
from brainstorming.models import Brainstorming, Idea, BrainstormingWatcher
from brainstorming.serializers import BrainstormingSerializer, IdeaSerializer
from brainstorming.user_session import update_bs_history, BS_HISTORY_KEY
from django.shortcuts import render
from django.http import Http404
from django.views.decorators.csrf import ensure_csrf_cookie

logger = logging.getLogger(__name__)


def _get_context(session, brainstorming_id=None):
    # copy history pks to append current
    bs_pks = session.get(BS_HISTORY_KEY, [])[:]
    if brainstorming_id:
        bs_pks.append(brainstorming_id)
    brainstorming_serializer = BrainstormingSerializer(Brainstorming.objects.filter(pk__in=bs_pks), many=True)
    brainstorming_store = {}
    idea_store = {}

    for bs in brainstorming_serializer.data:
        bid = bs['id']
        brainstorming_store[bid] = bs
        for idea in IdeaSerializer(Idea.objects.filter(brainstorming__pk=bid), many=True).data:
            if bid not in idea_store:
                idea_store[bid] = {}
            idea_store[bid][idea['id']] = idea

    context = {
        'email': session.get('email', ''),
        'name': session.get('name', ''),
        'brainstormingStore': json.dumps(brainstorming_store),
        'ideaStore': json.dumps(idea_store),
        'recentBrainstormings': json.dumps(session.get(BS_HISTORY_KEY, []))
    }

    return context


def _set_error(context, msg):
    context['error'] = msg


@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html', _get_context(request.session))


@ensure_csrf_cookie
def brainstorming(request, brainstorming_id):
    if not Brainstorming.objects.filter(pk=brainstorming_id).count():
        raise Http404

    update_bs_history(request.session, brainstorming_id)

    return render(request, 'index.html', _get_context(request.session, brainstorming_id))


@ensure_csrf_cookie
def notification(request, brainstorming_id):
    if not Brainstorming.objects.filter(pk=brainstorming_id).count():
        raise Http404

    update_bs_history(request.session, brainstorming_id)
    context = _get_context(request.session, brainstorming_id)

    email = get_verified_email(request)

    if not email:
        _set_error(context, 'Invalid activation request')
    else:
        watcher = get_object_or_None(BrainstormingWatcher, brainstorming__id=brainstorming_id, email=email)
        if watcher:
            watcher.delete()
        else:
            BrainstormingWatcher.objects.create(brainstorming=brainstorming_id, email=email)

    return render(request, 'index.html', context)