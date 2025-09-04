from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def test_view(request):
    return HttpResponse("Django is working! <a href='/login/'>Go to Login</a> | <a href='/register/'>Go to Register</a>")

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'auth/login.html')

def register_view(request):
    if request.method == 'POST':
        from users.models import User
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            User.objects.create_user(email=email, password=password, name=name)
            messages.success(request, 'Registration successful! Please login.')
            return redirect('/login/')
    
    return render(request, 'auth/register.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('/login/')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    from patients.models import Patient
    from doctors.models import Doctor
    
    patients = Patient.objects.filter(created_by=request.user)
    doctors = Doctor.objects.all()
    
    return render(request, 'dashboard.html', {
        'patients': patients,
        'doctors': doctors
    })

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("", test_view, name="test"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard_view, name="dashboard"),
    
    path("patients/", include("patients.urls")),
    path("doctors/", include("doctors.urls")),
    path("mappings/", include("mappings.urls")),
]
