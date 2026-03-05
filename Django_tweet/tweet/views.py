from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm,UserRegisterForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Chat,ChatMessage
from .ChatForm import ChatForm
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('created_at')
    return render(request,'tweet_list.html',{'tweets':tweets})

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')        
    else:
        form = TweetForm()
    return render(request,'tweet_form.html',{'form':form})

@login_required 
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=='POST':
        form = TweetForm(request.POST,request.FILES,instance=tweet)
        
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')   
    else:
        form = TweetForm(instance=tweet)
    return render(request,'tweet_form.html',{'form':form})
@login_required
def tweet_delete(request, tweet_id):
    tweet= get_object_or_404(Tweet, pk= tweet_id, user = request.user)
    if request.method=="POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',{'tweet':tweet})

def register(request):
    if request.method=="POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form = UserRegisterForm()
    return render(request,'registration/register.html',{'form': form})

@login_required
def chat(request):
    return render(request,'chat_list.html')

@login_required
def chat_list(request):
    current_user = request.user# Get the current user

    users = User.objects.exclude(id=current_user.id)# Get all users except the current user

    chats = Chat.objects.filter(users=current_user)# Get all chats involving the current user

    return render(
        request,
        'chat_list.html',
        {
            'users': users,
            'chats': chats
        }
    )

@login_required
def start_chat(request, user_id):
    current_user = request.user
    other_user = get_object_or_404(User, id=user_id)#if other user does not exist, return 404 error

    chat = Chat.objects.filter(users=current_user).filter(users=other_user).first()# Get the chat between the current user and the other user

    if not chat:
        chat = Chat.objects.create()
        chat.users.add(current_user, other_user)

    return redirect('chat_box', chat_id=chat.id)
@login_required
def chat_box(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)# Get the chat with the given ID or return 404 error if it does not exist
    if request.user not in chat.users.all():# Check if the current user is a participant in the chat
        return redirect('chat_list')# Redirect to the chat list if the current user is not a participant in the chat
    messages = chat.messages.order_by('created_at')
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.chat = chat
            msg.user = request.user
            msg.save()
            return redirect('chat_box', chat_id=chat.id)
    else:
        form = ChatForm()

    return render(
        request,
        'chat_box.html',
        {
            'chat': chat,
            'messages': messages,
            'form': form
        }
    )
