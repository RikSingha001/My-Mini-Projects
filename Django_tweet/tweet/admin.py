from django.contrib import admin
from .models import Tweet , Chat, ChatMessage

admin.site.register(Tweet)
admin.site.register(Chat)
admin.site.register(ChatMessage)

# Register your models here.
