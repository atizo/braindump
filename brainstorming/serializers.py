from api.fields import HTMLTextField, EscapedTextField, HyphenatedTextField
from brainstorming.models import Brainstorming, Idea, BrainstormingWatcher, IDEA_COLORS
from brainstorming.permissions import can_edit_brainstorming, rated_idea, can_edit_idea
from rest_framework import serializers, fields
from rest_framework.fields import DateTimeField


class BrainstormingSerializer(serializers.ModelSerializer):
    created = DateTimeField(read_only=True)
    question = HyphenatedTextField()
    details = HyphenatedTextField(required=False)
    detailsHTML = HTMLTextField(source='details', read_only=True)
    creatorEmail = fields.EmailField(source='creator_email',
                                     write_only=True)
    url = fields.Field('get_absolute_url')
    canEdit = serializers.SerializerMethodField('get_can_edit')

    class Meta:
        model = Brainstorming
        fields = (
            'id',
            'created',
            'question',
            'details',
            'detailsHTML',
            'creatorEmail',
            'url',
            'canEdit'
        )

    def get_can_edit(self, obj):
        return can_edit_brainstorming(self.context.get('request', None), obj.pk)


class IdeaSerializer(serializers.ModelSerializer):
    created = DateTimeField(read_only=True)
    title = fields.WritableField(required=False)
    text = EscapedTextField()
    textHTML = HTMLTextField(source='text', read_only=True)
    creatorName = fields.WritableField(source='creator_name', required=False)
    rated = serializers.SerializerMethodField('get_rated')
    color = fields.CharField(read_only=True)
    canEdit = serializers.SerializerMethodField('get_can_edit')
    image = serializers.SerializerMethodField('get_image')
    colorCode = serializers.SerializerMethodField('get_color_code')
    canEdit = serializers.SerializerMethodField('get_can_edit')

    class Meta:
        model = Idea
        fields = (
            'id',
            'created',
            'brainstorming',
            'title',
            'text',
            'textHTML',
            'creatorName',
            'ratings',
            'rated',
            'color',
            'colorCode',
            'image',
            'canEdit'
        )

    def get_can_edit(self, obj):
        return can_edit_idea(self.context.get('request', None), obj.pk)

    def get_image(self, obj):
        return obj.image.url

    def get_rated(self, obj):
        return rated_idea(self.context.get('request', None), obj.pk)

    def get_color_code(self, obj):
        if obj.color not in IDEA_COLORS:
            return 'c0'
        return 'c{0}'.format(IDEA_COLORS.index(obj.color) + 1)

    def save(self, **kwargs):
        request = self.context['request']

        # add file
        if 'imagefile' in request.FILES:
            self.object.image = request.FILES.get('imagefile')

        # remove file if filename in request is empty:
        if 'imagefile' in request.DATA and not len(request.DATA['imagefile']):
            self.object.image = None


        return super(IdeaSerializer, self).save(**kwargs)


class BrainstormingWatcherSerializer(serializers.ModelSerializer):
    email = fields.EmailField(write_only=True, required=False)

    class Meta:
        model = BrainstormingWatcher
        fields = (
            'email',
        )