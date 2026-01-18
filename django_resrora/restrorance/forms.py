from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import Review
from .models import Booking, RoomType
from django.utils.timezone import now
from datetime import timedelta, date


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'email', 'review']

class BookingForm(forms.ModelForm):
    room_type = forms.ModelChoiceField(
        queryset=RoomType.objects.all(),
        empty_label="Select Room Type"
    )
    

    class Meta:
        model = Booking
        fields = ['room_type', 'check_in', 'check_out', 'guests']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        today = now().date()

        if not check_in or not check_out:
            return cleaned_data

        # same-day / 4 hours rule
        if check_in == today:
            raise forms.ValidationError("Booking must be at least 4 hours in advance")

        # 3 months advance booking limit
        if check_in > today + timedelta(days=90):
            raise forms.ValidationError("Booking not allowed more than 3 months in advance")

        # invalid range
        if check_out <= check_in:
            raise forms.ValidationError("Invalid check-in / check-out range")

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔥 AUTO LOAD FROM MySQL EVERY TIME
        self.fields['room_type'].queryset = RoomType.objects.all()
        self.fields['room_type'].empty_label = "Select Room Type"