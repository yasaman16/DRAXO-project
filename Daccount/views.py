
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Dorder.models import Order

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "حساب با موفقیت ساخته شد!")
            return redirect('Dpages:home') # بعد از ثبت نام میره صفحه اصلی
    else:
        form = SignUpForm()
    return render(request, 'Daccount/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('Dpages:home') # بعد از لاگین میره صفحه اصلی
    else:
        form = LoginForm()
    return render(request, 'Daccount/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('Dpages:home')

@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).exclude(status='cart').order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'Daccount/profile.html', context)
