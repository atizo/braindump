from brainstorming.models import Brainstorming, Idea
from rest_framework import serializers, fields


class BrainstormingSerializer(serializers.ModelSerializer):
    question = fields.WritableField()
    details = fields.WritableField(required=False)
    creatorEmail = fields.WritableField(source='creator_email',
        write_only=True, required=False)

    class Meta:
        model = Brainstorming
        fields = (
            'slug',
            'created',
            'question',
            'details',
            'creatorEmail',
        )


class IdeaSerializer(serializers.ModelSerializer):
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