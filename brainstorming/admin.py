from django.contrib import admin
from brainstorming.models import Brainstorming, Idea, BrainstormingWatcher, EmailVerification


class BrainstormingAdmin(admin.ModelAdmin):
    list_display = ('question', 'creator_email', 'idea_sequence', 'created')
    readonly_fields = ('id', 'created', 'modified', 'creator_ip')
    search_fields = ['question', 'details', 'creator_email']


class IdeaAdmin(admin.ModelAdmin):
    list_display = ('text', 'number', 'brainstorming', 'creator_name', 'ratings', 'created')
    readonly_fields = ('id', 'created', 'modified', 'creator_ip')
    search_fields = ['text', 'title', 'creator_name', 'brainstorming__question']


class BrainstormingWatcherAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created', 'modified')

class EmailVerificationAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created', 'modified')


admin.site.register(Brainstorming, BrainstormingAdmin)
admin.site.register(Idea, IdeaAdmin)
admin.site.register(BrainstormingWatcher, BrainstormingWatcherAdmin)
admin.site.register(EmailVerification, EmailVerificationAdmin)