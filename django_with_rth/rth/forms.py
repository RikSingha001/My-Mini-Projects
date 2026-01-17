from django import forms
from .models import  Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['meal_type', 'total_price']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = [ 'order', 'item_name', 'price', 'quantity']

