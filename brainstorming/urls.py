from django.conf.urls import patterns, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('brainstorming.views',
    url(r'^$', 'index', name='home'),
    url(r'^(?P<brainstorming_slug>\w{12})/?', 'brainstorming', name='brainstorming'),
    url(r'^.*$', TemplateView.as_view(template_name="index.html")),
) 