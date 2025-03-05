from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from core.models import User  # Import your User model

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            
            # Redirect based on user role
            if user.is_superuser:
                return redirect("admin_dashboard")
            else:
                return redirect("user_dashboard")
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, "core/login.html")


def logout_view(request):
    logout(request)
    return redirect('login')
