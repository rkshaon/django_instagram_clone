from django.contrib import admin

from stories.models import *

admin.site.register(Story)
admin.site.register(StoryStream)
