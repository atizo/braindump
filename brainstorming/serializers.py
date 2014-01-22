from brainstorming.models import Brainstorming, Idea
from rest_framework import serializers, fields


class BrainstormingSerializer(serializers.ModelSerializer):
    creatorEmail = fields.Field(source='creator_email')

    def convert_object(self, obj):
        """Remove email field when serializing an object"""
        del self.fields['creatorEmail']

        return super(BrainstormingSerializer, self).convert_object(obj)

    class Meta:
        model = Brainstorming
        fields = (
            'id',
            'created',
            'question',
            'details',
            'creatorEmail',
            #'image',
        )


class IdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = (
            'id',
            'created',
            'title',
            'text',
            #'image',
        )