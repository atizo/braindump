from api.forms import TimeZoneAwareDateTimeField
from brainstorming.models import Brainstorming, Idea
from rest_framework import serializers, fields


class BrainstormingSerializer(serializers.ModelSerializer):
    created = TimeZoneAwareDateTimeField(read_only=True)
    question = fields.WritableField()
    details = fields.WritableField(required=False)
    creatorEmail = fields.WritableField(source='creator_email',
        write_only=True, required=False)
    url = fields.Field('get_absolute_url')

    class Meta:
        model = Brainstorming
        fields = (
            'slug',
            'created',
            'question',
            'details',
            'creatorEmail',
            'url'
        )


class IdeaSerializer(serializers.ModelSerializer):
    created = TimeZoneAwareDateTimeField(read_only=True)
    title = fields.WritableField()
    text = fields.WritableField()

    class Meta:
        model = Idea
        fields = (
            'id',
            'created',
            'title',
            'text',
        )