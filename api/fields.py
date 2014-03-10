import bleach
from django.utils.html import linebreaks
from rest_framework import serializers


class EscapedTextField(serializers.WritableField):
    def to_native(self, obj):
        return bleach.clean(obj, tags=[])


class HTMLTextField(serializers.WritableField):
    def __init__(self, break_lines=True, *args, **kwargs):
        self._break_lines = break_lines

        super(HTMLTextField, self).__init__(*args, **kwargs)

    def to_native(self, obj):
        clean = bleach.linkify(bleach.clean(obj, tags=[]))
        if self._break_lines:
            return linebreaks(clean)
        return clean