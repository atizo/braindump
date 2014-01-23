from django.contrib import admin
from brainstorming.models import Brainstorming


class BrainstormingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Brainstorming, BrainstormingAdmin)