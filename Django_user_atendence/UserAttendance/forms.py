from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from UserAttendance.models import UserAttendance

# class UserRegisterForm(UserCreationForm):
#     number = forms.CharField(max_length=15)
#     image = forms.ImageField(required=False)

#     class Meta:
#         model = User
#         fields = [
#             "username",
#             "number",
#             "password1",
#             "image",
#             "password2",
#         ]


class AttendanceForm(forms.ModelForm):

    class Meta:
        model = UserAttendance

        fields = [
            "image",
            "latitude",
            "longitude",
            "location",
        ]

        widgets = {
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
            "location": forms.HiddenInput(),
        }

from .models import (
    UserAttendance,
    LeaveApplication,
    ResignationApplication,
)

class LeaveApplicationForm(forms.ModelForm):

    class Meta:

        model = LeaveApplication

        fields = [
            "leave_type",
            "start_date",
            "end_date",
            "reason",
        ]

        widgets = {

            "leave_type": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "reason": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder":
                        "Reason for leave"
                }
            ),
        }

class ResignationApplicationForm(forms.ModelForm):

    class Meta:
        model = ResignationApplication

        fields = [
            "resignation_date",
            "reason",
        ]

        widgets = {
            "resignation_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "reason": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": "form-control",
                    "placeholder": "Enter your resignation reason"
                }
            ),
        }
class AttendanceOutForm(forms.ModelForm):

    class Meta:
        model = UserAttendance

        fields = [
            "out_image",
            "out_latitude",
            "out_longitude",
            "out_location",
        ]

        widgets = {
            "out_image": forms.HiddenInput(),

            "out_latitude": forms.HiddenInput(),
            "out_longitude": forms.HiddenInput(),
            "out_location": forms.HiddenInput(),
        }