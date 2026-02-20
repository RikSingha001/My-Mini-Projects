from django.contrib import admin
from .models import User, LoginHistory, search, ChatRoom, Message , Profile
admin.site.register(User)
admin.site.register(LoginHistory)
admin.site.register(search)
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(Profile)
