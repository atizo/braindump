from urlparse import urljoin
from django.contrib.sites.models import Site


def get_full_url(path=None):
    current_site = Site.objects.get_current()
    url = 'http://{domain}'.format(domain=current_site.domain)
    if path:
        url = urljoin(url, path)
    return url