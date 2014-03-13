import bleach
from django.utils.html import linebreaks
import pyphen
from rest_framework import serializers
import lxml.html

hyphenator = pyphen.Pyphen(lang='de')


class EscapedTextField(serializers.WritableField):
    def to_native(self, obj):
        return bleach.clean(obj, tags=[])


class HyphenatedTextField(serializers.WritableField):
    def from_native(self, value):
        return value.replace(u'\u00AD', '')

    def to_native(self, obj):
        return hyphenator.inserted(obj, u'\u00AD')


class HTMLTextField(serializers.WritableField):
    def to_native(self, obj):
        if not len(obj):
            return obj

        clean = bleach.linkify(bleach.clean(obj, tags=[]))

        dom = lxml.html.fromstring(clean)

        for q in dom.iter():
            if q.text:
                q.text = hyphenator.inserted(q.text, u'\u00AD')
            if q.tail:
                q.tail = hyphenator.inserted(q.tail, u'\u00AD')

        return linebreaks(lxml.html.tostring(dom))