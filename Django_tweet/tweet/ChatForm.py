from django import forms
from .models import ChatMessage

class ChatForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']

