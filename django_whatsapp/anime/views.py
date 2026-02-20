from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import User, LoginHistory, ChatRoom, Message, Profile


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
    current_user = request.user

    rooms = ChatRoom.objects.filter(
        Q(user1=current_user) | Q(user2=current_user)
    ).order_by("-created_at")

    if request.method == "POST":
        phone = request.POST.get("phone")

        if not phone:
            return render(request, "home.html", {
                "rooms": rooms,
                "error": "Enter phone number"
            })

        try:
            other_user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            return render(request, "home.html", {
                "rooms": rooms,
                "error": "User not found"
            })

        if other_user == current_user:
            return render(request, "home.html", {
                "rooms": rooms,
                "error": "You cannot chat with yourself"
            })

        room = ChatRoom.objects.filter(
            Q(user1=current_user, user2=other_user) |
            Q(user1=other_user, user2=current_user)
        ).first()

        if not room:
            room = ChatRoom.objects.create(
                user1=current_user,
                user2=other_user
            )

        return redirect("chat_room", room.id)

    return render(request, "home.html", {
        "rooms": rooms
    })


@login_required
def chat_room(request, room_id):
    room = ChatRoom.objects.get(id=room_id)
    messages = room.messages.all().order_by("timestamp")

    if request.method == "POST":
        text = request.POST.get("text")
        photo = request.FILES.get("photo")

        if text or photo:
            Message.objects.create(
                room=room,
                sender=request.user,
                text=text,
                photo=photo
            )

        return redirect("chat_room", room_id=room.id)

    return render(request, "chat_room.html", {
        "room": room,
        "messages": messages
    })

@login_required
def profile_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        photo = request.FILES.get("photo")
        print("FILES:", request.FILES)

        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.name = name
        if photo:
            profile.photo = photo
        profile.save()

        return redirect("profile")

    profile = Profile.objects.filter(user=request.user).first()
    return render(request, "profile.html", {"profile": profile})