from django.contrib import admin
from brainstorming.models import Brainstorming, Idea, BrainstormingWatcher


class BrainstormingAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created', 'modified', 'creator_ip')


class IdeaAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created', 'modified', 'creator_ip')


class BrainstormingWatcherAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created', 'modified')


admin.site.register(Brainstorming, BrainstormingAdmin)
admin.site.register(Idea, IdeaAdmin)
admin.site.register(BrainstormingWatcher, BrainstormingWatcherAdmin)