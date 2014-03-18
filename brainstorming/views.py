import json
import logging

from braindump.env import get_full_url
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
from django.http import HttpResponse
from xlsxwriter.workbook import Workbook
from pytz import timezone


try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

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


def export(request, brainstorming_id):
    if not Brainstorming.objects.filter(pk=brainstorming_id).exists():
        raise Http404

    bs = Brainstorming.objects.get(pk=brainstorming_id)

    user_tz = timezone(request.COOKIES.get('timezone', ''))

    # create a workbook in memory
    output = StringIO.StringIO()

    book = Workbook(output)
    sheet = book.add_worksheet('Brainstroming')
    bold = book.add_format({'bold': True})
    date_format = book.add_format({'num_format': 'dd/mm/yy HH:mm'})

    sheet.write(0, 0, 'Number', bold)
    sheet.write(0, 1, 'Title', bold)
    sheet.write(0, 2, 'Text', bold)
    sheet.write(0, 3, 'Author', bold)
    sheet.write(0, 4, 'Ratings', bold)
    sheet.write(0, 5, 'Created Date', bold)
    sheet.write(0, 6, 'Image', bold)

    sheet.set_column(1, 1, 20)
    sheet.set_column(2, 2, 40)
    sheet.set_column(5, 5, 20)
    sheet.set_column(6, 6, 50)

    for i, idea in enumerate(Idea.objects.filter(brainstorming=bs), 1):
        sheet.write(i, 0, idea.number)
        sheet.write(i, 1, idea.title)
        sheet.write(i, 2, idea.text)
        sheet.write(i, 3, idea.creator_name or ' ')
        sheet.write_number(i, 4, idea.ratings)
        sheet.write_datetime(i, 5, idea.created.astimezone(user_tz).replace(tzinfo=None), date_format)
        if idea.image:
            sheet.write_url(i, 6, get_full_url(idea.image.url))

    book.close()

    # construct response
    output.seek(0)
    response = HttpResponse(output.read(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=test.xlsx"

    return response