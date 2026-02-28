from django.contrib import admin
from .models import User, LoginHistory
from .models import  ChatRequest, ChatResponse, Task

# Register your models here.
admin.site.register(User)
admin.site.register(LoginHistory)
admin.site.register(ChatRequest)
admin.site.register(ChatResponse) 
admin.site.register(Task)
