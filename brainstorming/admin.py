from django.contrib import admin
from brainstorming.models import Brainstorming


class BrainstormingAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'created', 'modified')


admin.site.register(Brainstorming, BrainstormingAdmin)