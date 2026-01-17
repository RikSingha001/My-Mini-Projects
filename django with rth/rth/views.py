from urllib import request
from django.shortcuts import render
from .forms import UserRegisterForm
from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from .models import Order, OrderItem
from datetime import datetime 
from .item_manu import MenuManager


# Create your views here.
def sing(request):
    return render(request, 'sing.html')

@login_required
def home_page(request):
    menu = MenuManager()

    if request.method == "POST":
        order = Order.objects.create(
            user=request.user,
            meal_type=menu.meal_type,
            total_price=0
        )

        total = 0
        for name, price in menu.choices.items():
            qty = int(request.POST.get(f"qty_{name}", 0))
            if qty > 0:
                OrderItem.objects.create(
                    order=order,
                    item_name=name,
                    price=price,
                    quantity=qty
                )
                total += price * qty

        order.total_price = total
        order.save()

        # ✅ PASS order_id
        return redirect("conform_order", order_id=order.id)

    return render(request, "home.html", {
        "items": menu.choices,
        "meal_type": menu.meal_type,
        "status": menu.status
    })



def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password1'])
            user.save()
            auth_login(request, user)
            return redirect('home_page')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})
def logout(request):
    return render(request, 'registration/logout.html')
 
@login_required
def booking(request):
    item = Order.objects.filter(user=request.user).order_by('-created_at')
    user = request.user
    total_price = sum(order.total_price for order in item)

    return render(request, 'booking.html', {'item':item, 'total_price':total_price})

@login_required
def conform_order(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if order.status == 'Pending':
        order.status = 'Confirmed'
        order.save()

    return render(request, 'conform_order.html', {'order': order})

def about(request):
    return render(request, 'about.html')