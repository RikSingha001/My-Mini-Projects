from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login
from .models import User, LoginHistory , Hospital, EmergencyRequest, Hospital_registration, ambulance_driver_registration, MatchedAmbulance , ambulance_login, Duty_onOff_modes
from django.contrib.auth.decorators import login_required
import random
from django.db.models import Q
import string
# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def home(request):

    if request.method == "POST":

        state = request.POST.get("state")
        city = request.POST.get("city")
        address = request.POST.get("full_address")
        emergency_type = request.POST.get("emergency_type")

        emergency = EmergencyRequest.objects.create(
            user=request.user,
            state=state,
            city=city,
            full_address=address,
            emergency_type=emergency_type
        )

        hospital = Hospital_registration.objects.first()

        return redirect(
            "matched_ambulance",
            hospital_id=hospital.id,
            emergency_id=emergency.id
)

    return render(request, "home.html")
        

    


def login_view(request):

    if request.method == "POST":

        phone = request.POST.get("phone_number")

        if not phone:
            return render(request, "login.html", {
                "error": "Phone number required"
            })

        user, created = User.objects.get_or_create(
            phone_number=phone
        )

        LoginHistory.objects.create(
            phone_number=phone
        )

        login(
            request,
            user,
            backend='django.contrib.auth.backends.ModelBackend'
        )

        return redirect("home")

    return render(request, "login.html")


def registration_hospital(request):

    if request.method == "POST":
        ambulance_key_code = ''.join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=8
            )
        )
    

        hospital = Hospital_registration.objects.create(

            hospital_name=request.POST.get("hospital_name"),

            hospital_address=request.POST.get("hospital_address"),

            hospital_phone=request.POST.get("hospital_phone"),

            ambulance_key_code=ambulance_key_code
        )

        return render(request, "registration_success.html", {
            "hospital": hospital
        })

    return render(request, "hospital_registration.html")
def ambulance_registration(request):

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        ambulance_number = request.POST.get("ambulance_number")
        ambulance_key_code = request.POST.get("ambulance_key_code")
        ambulance_service_type=request.POST.get("ambulance_service_type")


        try:

            hospital = Hospital_registration.objects.get(
                ambulance_key_code=ambulance_key_code
            )

            ambulance_driver_registration.objects.create(
                name=name,
                phone=phone,
                ambulance_number=ambulance_number,
                ambulance_key_code=ambulance_key_code,
                ambulance_service_type=ambulance_service_type,
                hospital=hospital
            )

            return render(request, "ambulance_success.html", {
                "hospital": hospital
            })

        except Hospital_registration.DoesNotExist:

            return render(request, "ambulance_registration.html", {
                "error": "Invalid Key Code"
            })

    return render(request, "ambulance_registration.html")


def ambulance_login_view(request):

    if request.method == "POST":

        phone = request.POST.get("phone")

        driver = ambulance_driver_registration.objects.filter(
            phone=phone
        ).first()

        if driver:

            ambulance_login.objects.create(
                phone=phone
            )

            # SESSION SAVE
            request.session["ambulance_phone"] = phone

            return redirect("ambulance_dashboard")

        return render(request, "ambulance_login.html", {
            "error": "Invalid phone number"
        })

    return render(request, "ambulance_login.html")
def ambulance_dashboard(request):

    phone = request.session.get("ambulance_phone")

    if not phone:
        return redirect("ambulance_login_view")

    driver = ambulance_driver_registration.objects.filter(
        phone=phone
    ).first()

    if not driver:
        return redirect("ambulance_login_view")

    duty_status, created = Duty_onOff_modes.objects.get_or_create(
        ambulance_driver=driver
    )

    if request.method == "POST":

        duty_status.is_on_duty = not duty_status.is_on_duty
        duty_status.save()

        return redirect("ambulance_dashboard")

    return render(request, "ambulance_dashboard.html", {
        "driver": driver,
        "duty_status": duty_status
    })

@login_required
def matched_ambulance(request, hospital_id, emergency_id):

    hospital = get_object_or_404(
        Hospital_registration,
        id=hospital_id
    )

    emergency = get_object_or_404(
        EmergencyRequest,
        id=emergency_id
    )

    matched_ambulances = ambulance_driver_registration.objects.filter(
        hospital=hospital,
        duty_status__is_on_duty=True
    ).filter(
        Q(ambulance_service_type=emergency.emergency_type) |
        Q(ambulance_service_type="All")
    ).distinct()

    return render(request, "matched_ambulance.html", {
        "matched_ambulances": matched_ambulances,
        "emergency": emergency
    })