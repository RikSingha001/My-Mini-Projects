from urllib import request

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# from .client import HanabiClient
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


# @login_required
# def home(request):
#     ai_response = None
#     error_message = None

#     if request.method == "POST":
#         user_message = request.POST.get("message")

#         if user_message:
#             try:
#                 client = HanabiClient()
#                 ai_response = client.get_response(user_message)

#                 Ai_Assistant.objects.create(
#                     user=request.user,
#                     message=user_message,
#                     response=ai_response
#                 )

#             except RateLimitError:
#                 error_message = "API limit reached. Try again later."

#             except Exception as e:
#                 error_message = "Something went wrong."

#     chats = Ai_Assistant.objects.filter(
#         user=request.user
#     ).order_by("timestamp")

#     return render(request, "home.html", {
#         "chats": chats,
#         "error": error_message
#     })

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
