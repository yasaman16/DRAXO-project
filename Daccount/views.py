
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm, LoginForm
from django.contrib import messages

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
