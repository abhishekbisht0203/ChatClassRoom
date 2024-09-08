from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(SubTopic)
admin.site.register(Note)
admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(ChatMessage)