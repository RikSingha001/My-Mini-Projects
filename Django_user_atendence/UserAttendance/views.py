

# def register(request):
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("login")

#     else:
#         form = UserRegisterForm()

#     return render(request, "register.html", {"form": form})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import AttendanceForm, ResignationApplicationForm,LeaveApplicationForm ,AttendanceOutForm
from .models import LeaveApplication, LeaveBalance, LoginLogoutLog, ResignationApplication, UserAttendance, LeaveBalance
from datetime import date , datetime 
from django.utils import timezone
from django.contrib import messages



def index(request):
    return render(request, "index.html")


def get_client_ip(request):

    x_forwarded_for = request.META.get(
        "HTTP_X_FORWARDED_FOR"
    )

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]

    else:
        ip = request.META.get(
            "REMOTE_ADDR"
        )

    return ip


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            LoginLogoutLog.objects.create(
                user=user,
                action="LOGIN",
                ip_address=get_client_ip(request),
                user_agent=request.META.get(
                    "HTTP_USER_AGENT",
                    ""
                )
            )

            return redirect("dashboard")

        return render(
            request,
            "login.html",
            {
                "message":
                    "Invalid username or password"
            }
        )

    return render(
        request,
        "login.html"
    )

@login_required
def dashboard(request):

    return render(
        request,
        "dashboard.html"
    )

@login_required
def attendance_sum(request):

    if request.method == "POST":

        form = AttendanceForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            attendance = form.save(commit=False)

            attendance.user = request.user

            attendance.save()

            messages.success(
                request,
                "Attendance IN saved successfully."
            )

            return redirect("attendance_sum")

        else:
            print("ATTENDANCE IN ERRORS:", form.errors)

    else:
        form = AttendanceForm()

    out_form = AttendanceOutForm()

    return render(
        request,
        "attendance_sum.html",
        {
            "form": form,
            "out_form": out_form,
        }
    )



@login_required
def logout_view(request):

    # Save Logout History BEFORE logout
    LoginLogoutLog.objects.create(
        user=request.user,
        action="Logout",
        ip_address=get_client_ip(request),
        user_agent=request.META.get(
            "HTTP_USER_AGENT",
            ""
        )
    )

    # Logout
    logout(request)

    return redirect("login")


@login_required
def profile(request):

    profile_data = request.user.profile

    leave_balance = LeaveBalance.objects.filter(
        user=request.user
    ).first()

    return render(
        request,
        "profile.html",
        {
            "profile": profile_data,
            "leave_balance": leave_balance,
        }
    )

@login_required
def leave_application(request):

    leave_balance = LeaveBalance.objects.filter(
        user=request.user
    ).first()

    if request.method == "POST":

        form = LeaveApplicationForm(
            request.POST
        )

        if form.is_valid():

            leave = form.save(
                commit=False
            )

            leave.user = request.user

            # Calculate days
            days = (
                leave.end_date -
                leave.start_date
            ).days + 1

            if days <= 0:

                form.add_error(
                    "end_date",
                    "End date must be after start date."
                )

            else:

                # Check balance
                available = 0

                if leave.leave_type == "CL":
                    available = leave_balance.cl

                elif leave.leave_type == "EL":
                    available = leave_balance.el

                elif leave.leave_type == "SL":
                    available = leave_balance.sl

                if days > available:

                    form.add_error(
                        "start_date",
                        f"Only {available} days available."
                    )

                else:

                    leave.days = days

                    leave.save()

                    return redirect(
                        "leave_application"
                    )

    else:

        form = LeaveApplicationForm()

    # Existing applications
    leave_history = LeaveApplication.objects.filter(
        user=request.user
    ).order_by(
        "-applied_at"
    )

    return render(
        request,
        "leave_application.html",
        {
            "form": form,
            "leave_balance": leave_balance,
            "leave_history": leave_history,
        }
    )
@login_required
def attendance_history(request):

    records = UserAttendance.objects.filter(
        user=request.user
    ).order_by(
        "-date",
        "-time"
    )

    return render(
        request,
        "attendance_history.html",
        {
            "records": records
        }
    )

@login_required
def resign_application(request):

    if request.method == "POST":

        form = ResignationApplicationForm(request.POST)

        if form.is_valid():

            resignation = form.save(commit=False)

            resignation.user = request.user

            resignation.save()

            return redirect("resign_application")

    else:

        form = ResignationApplicationForm()

    resignations = ResignationApplication.objects.filter(
        user=request.user
    ).order_by(
        "-applied_at"
    )

    return render(
        request,
        "resign_application.html",
        {
            "form": form,
            "resignations": resignations,
        }
    )


@login_required
def login_logout_history(request):

    logs = LoginLogoutLog.objects.filter(
        user=request.user
    ).order_by(
        "-timestamp"
    )

    return render(
        request,
        "login_logout_history.html",
        {
            "logs": logs
        }
    )

# @login_required
# def leave_history(request):

#     leaves = LeaveApplication.objects.filter(
#         user=request.user,
#         status="Approved"
#     ).order_by(
#         "-start_date"
#     )

#     return render(
#         request,
#         "leave_history.html",
#         {
#             "leaves": leaves
#         }
#     )


@login_required
def attendance_out(request):

    if request.method != "POST":
        return redirect("attendance_sum")

    attendance = UserAttendance.objects.filter(
        user=request.user,
        date=timezone.localdate(),
        out_at__isnull=True
    ).order_by("-time").first()

    if attendance is None:

        messages.error(
            request,
            "No active Attendance IN found."
        )

        return redirect("attendance_sum")


    out_image = request.FILES.get("out_image")

    if not out_image:

        messages.error(
            request,
            "OUT photo is required."
        )

        return redirect("attendance_sum")



    out_latitude = request.POST.get("out_latitude")
    out_longitude = request.POST.get("out_longitude")
    out_location = request.POST.get("out_location")



    attendance.out_image = out_image
    attendance.out_latitude = out_latitude
    attendance.out_longitude = out_longitude
    attendance.out_location = out_location
    attendance.out_at = timezone.now()

    attendance.save(
        update_fields=[
            "out_image",
            "out_latitude",
            "out_longitude",
            "out_location",
            "out_at",
        ]
    )

    print("========== ATTENDANCE OUT ==========")
    print("Attendance ID:", attendance.id)
    print("OUT IMAGE:", attendance.out_image.name)
    print("OUT LATITUDE:", attendance.out_latitude)
    print("OUT LONGITUDE:", attendance.out_longitude)
    print("OUT LOCATION:", attendance.out_location)
    print("OUT AT:", attendance.out_at)
    print("====================================")
    print("ATTENDANCE OUT SAVED:", attendance.id)

    messages.success(
        request,
        "Attendance OUT saved successfully."
    )

    return redirect("attendance_history")


