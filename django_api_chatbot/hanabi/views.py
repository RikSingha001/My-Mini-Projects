from urllib import request

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .utils import DetectMood, GenerateReply
from .models import  ChatRequest, ChatResponse, Task

from .models import User, LoginHistory

# Create your views here.
def index(request):
    return render(request, 'index.html')



def login_view(request):
    if request.method == "POST":
        phone = request.POST.get("phone")

        if not phone:
            return render(request, "login.html")

        user, created = User.objects.get_or_create(phone_number=phone)

        LoginHistory.objects.create(phone_number=phone)

        login(request, user)

        return redirect("home")
    return render(request, "login.html")


@login_required
def home(request):
    if request.method == "POST":
        message = request.POST.get("message")
        chat_request = ChatRequest.objects.create(message=message)

        detector = DetectMood(message)
        mood = detector.mood
        reply = GenerateReply.generate_reply(mood)
        ChatResponse.objects.create(
            request=chat_request,
            reply_main=reply["main"],
            reply_secondary=reply["secondary"]
        )

        return redirect("home")

    chats = ChatResponse.objects.all().order_by("-id")

    return render(request, "home.html", {
        "chats": chats
    })
