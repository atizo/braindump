from brainstorming.email_verification import send_email_verification
from django.core.urlresolvers import reverse
from rest_framework import permissions

PERMISSION_MAP = 'drf_permission_map'
PERMISSION_PROJECT = 'prj'
OWN_IDEA = 'drf_idea_list'
RATED_IDEAS = 'ratids'


class BrainstromPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        # List action is allowed only to admin users
        if view.action == 'list':
            return request.user and request.user.is_staff

        return True

    def has_object_permission(self, request, view, obj):
        # Allows access to admin users
        if request.user and request.user.is_staff:
            return True
        # Read and create permissions are allowed to any request,
        # so we'll always allow GET, HEAD, OPTIONS or POST requests
        if request.method in permissions.SAFE_METHODS + ['POST']:
            return True

        return obj.pk in request.session.get(PERMISSION_MAP, {}).get(PERMISSION_PROJECT, [])


def bs_set_edit_permission(request, bsid):
    if PERMISSION_MAP not in request.session:
        request.session[PERMISSION_MAP] = {}

    if PERMISSION_PROJECT not in request.session[PERMISSION_MAP]:
        request.session[PERMISSION_MAP][PERMISSION_PROJECT] = []

    if bsid not in request.session[PERMISSION_MAP][PERMISSION_PROJECT]:
        request.session[PERMISSION_MAP][PERMISSION_PROJECT].append(bsid)
        request.session.modified = True


def can_edit_bs(request, bsid):
    if request and PERMISSION_MAP in request.session and PERMISSION_PROJECT in request.session[PERMISSION_MAP]:
        return bsid in request.session[PERMISSION_MAP][PERMISSION_PROJECT]
    return False


def set_idea(request, iid):
    if OWN_IDEA not in request.session:
        request.session[OWN_IDEA] = []

    if iid not in request.session[OWN_IDEA]:
        request.session[OWN_IDEA].append(iid)
        request.session.modified = True


def get_is_own_idea(request, iid):
    if request and OWN_IDEA in request.session:
        return iid in request.session[OWN_IDEA]
    return False


def rated_idea(request, iid):
    if request and RATED_IDEAS in request.session:
        return iid in request.session[RATED_IDEAS]
    return False


def edit_mode(brainstorming, email):
    url = reverse('edit', kwargs={'brainstorming_id': brainstorming.pk})
    status = 'ban'

    if email == brainstorming.creator_email:
        status = 'edit'
        send_email_verification(to=email,
                                subject='Edit your brainstorming',
                                callback=url,
                                template='brainstorming/mails/edit.txt',
                                context={'brain': brainstorming}
        )

    return {'status': status}