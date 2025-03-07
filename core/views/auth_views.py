from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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

@login_required
def profile_view(request):
    user = request.user  # Get the currently logged-in user

    if request.method == "POST":
        user.fullname = request.POST.get("fullname")
        user.email = request.POST.get("email")
        user.phonenumber = request.POST.get("phonenumber")
        user.address = request.POST.get("address")

        user.save()
        messages.success(request, "Profile updated successfully!")

        return redirect("profile")  # Refresh the page after update

    return render(request, "core/profile.html", {"user": user})

@login_required
def password_change(request):
    user = request.user  # Get the currently logged-in user

    if request.method == "POST":
        current_password = request.POST.get("current_password")  # Fetch current password
        new_password = request.POST.get("new_password")  # Fetch new password
        confirm_password = request.POST.get("confirm_password")  # Fetch confirmation password

        # Check if current password is correct
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect("password_change")

        # Check if new password matches confirmation
        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return redirect("password_change")

        # Update password
        user.set_password(new_password)
        user.save()

        # Keep the user logged in after password change
        update_session_auth_hash(request, user)

        messages.success(request, "Password updated successfully!")
        return redirect("password_change")  # Redirect to profile after successful password change

    return render(request, "core/password.html", {"user": user})

def logout_view(request):
    logout(request)
    return redirect('login')
