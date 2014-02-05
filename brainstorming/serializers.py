from api.forms import TimeZoneAwareDateTimeField
from brainstorming.models import Brainstorming, Idea, BrainstormingWatcher
from rest_framework import serializers, fields


class BrainstormingSerializer(serializers.ModelSerializer):
    created = TimeZoneAwareDateTimeField(read_only=True)
    question = fields.WritableField()
    details = fields.WritableField(required=False)
    creatorEmail = fields.WritableField(source='creator_email',
        write_only=True)
    url = fields.Field('get_absolute_url')

    class Meta:
        model = Brainstorming
        fields = (
            'id',
            'created',
            'question',
            'details',
            'creatorEmail',
            'url'
        )


class IdeaSerializer(serializers.ModelSerializer):
    created = TimeZoneAwareDateTimeField(read_only=True)
    title = fields.WritableField(required=False)
    text = fields.WritableField()
    creatorName = fields.WritableField(source="creator_name", required=False)

    class Meta:
        model = Idea
        fields = (
            'id',
            'created',
            'brainstorming',
            'title',
            'text',
            'creatorName',
        )


class BrainstormingWatcherSerializer(serializers.ModelSerializer):
    email = fields.WritableField(write_only=True, required=False)

    class Meta:
        model = BrainstormingWatcher
        fields = (
            'email',
        )