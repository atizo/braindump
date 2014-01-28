from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
import os

admin.autodiscover()

urlpatterns = patterns('brainstorming.views',
                       url(r'^$', 'index', name='home'),
                       url(r'^invite$', TemplateView.as_view(template_name="index.html"), name='invite'),
                       url(r'^(?P<brainstorming_slug>\w{12})$', 'brainstorming', name='brainstorming'),
)