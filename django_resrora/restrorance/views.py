from django.shortcuts import redirect, render ,get_object_or_404
from django.contrib.auth import login 
from .forms import UserRegisterForm, BookingForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ReviewForm
# Create your views here.
from .models import Review, Booking
from django.utils.timezone import now
from datetime import date, timedelta
from .models import Booking, RoomType
from django.contrib.auth.decorators import login_required



def home_page(request):
    reviews = Review.objects.order_by('-id')[:3]  
    total_reviews = Review.objects.count()

    return render(request, 'home.html', {
        'reviews': reviews,
        'total_reviews': total_reviews
    })



def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            Profile.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )

            login(request, user)
            return redirect('home_page')
        else: 
            print(form.errors)  # DEBUG
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def logout(request):
    return render(request, 'registration/logout.html')


@login_required
def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('review')   # same page reload
    else:
        form = ReviewForm()

    return render(request, 'review.html', {'form': form})

@login_required
def all_reviews(request):
    reviews = Review.objects.order_by('-id')
    return render(request, 'all_reviews.html', {'reviews': reviews})

def is_room_available(room_type, check_in, check_out):
    """
    Returns True if there is at least one room available of the given type
    for the requested check-in/check-out dates.
    """
    booked_count = Booking.objects.filter(
        room_type=room_type,
        status='BOOKED',
        check_in__lt=check_out,
        check_out__gt=check_in
    ).count()

    return booked_count < room_type.total_rooms

@login_required
def available_rooms(room_type, check_in, check_out):
    booked = Booking.objects.filter(
        room_type=room_type,
        status='BOOKED',
        check_in__lt=check_out,
        check_out__gt=check_in
    ).count()

    return room_type.total_rooms - booked

@login_required
def create_booking(request):
    room_types = RoomType.objects.all()   # 🔥 MySQL থেকে direct

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user

            if not is_room_available(
                booking.room_type,
                booking.check_in,
                booking.check_out
            ):
                return render(request, 'booking.html', {
                    'form': form,
                    'room_types': room_types,
                    'error': 'No rooms available'
                })

            booking.save()
            return redirect('my_bookings')
    else:
        form = BookingForm()

    return render(request, 'booking.html', {
        'form': form,
        'room_types': room_types   # 🔥 IMPORTANT
    })
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'my_bookings.html', {
        'bookings': bookings
    })

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        status='BOOKED'
    )

    booking.status = 'CANCELLED'
    booking.save()

    return redirect('my_bookings')

@login_required
def check_out(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        status='BOOKED'
    )

    booking.status = 'CHECKED_OUT'
    booking.save()

    return redirect('my_bookings')
@login_required
def admin_summary(request):
    summary = []

    room_types = RoomType.objects.all()

    for rt in room_types:
        booked = Booking.objects.filter(room_type=rt, status='BOOKED').count()
        checked_out = Booking.objects.filter(room_type=rt, status='CHECKED_OUT').count()

        summary.append({
            'name': rt.name,
            'booked': booked,
            'checked_out': checked_out,
            'total': rt.total_rooms,
            'available': rt.total_rooms - booked
        })

    bookings = Booking.objects.all().order_by('-created_at')  # সব বুকিং দেখাতে চাইলে

    return render(request, 'admin_summary.html', {
        'summary': summary,
        'bookings': bookings
    })