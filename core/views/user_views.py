from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from core.models import User
import json

@login_required
def user_dashboard(request):
    if request.user.is_superuser:
        return render(request, "core/admin_dashboard.html")
    else:
        return render(request, "core/user_dashboard.html")

@login_required
def manage_users(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    users = User.objects.filter(is_superuser=False)
    return render(request, 'core/manage_users.html', {'users': users})

@csrf_exempt
@login_required
def add_user(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        address = request.POST.get('address')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        if User.objects.filter(phonenumber=phonenumber).exists():
            return JsonResponse({'error': 'Phone number already exists'}, status=400)
        user = User.objects.create_user(
            fullname=fullname,
            email=email,
            phonenumber=phonenumber,
            password=password,
            address=address
        )

        return JsonResponse({'success': 'User added successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def update_user(request, user_id):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.fullname = request.POST.get('fullname')
        user.email = request.POST.get('email')
        user.phonenumber = request.POST.get('phonenumber')
        user.address = request.POST.get('address')

        # Update password only if provided
        password = request.POST.get('password')
        if password:
            user.set_password(password)

        user.save()
        return JsonResponse({'success': 'User updated successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return JsonResponse({'success': 'User deleted successfully'})

@csrf_exempt
@login_required
def toggle_user_status(request, user_id):
    if request.method == "POST":
        try:
            user = User.objects.get(id=user_id)
            data = json.loads(request.body)
            user.is_active = data["is_active"]
            user.save()
            return JsonResponse({"success": True, "is_active": user.is_active})
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "User not found"}, status=404)
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)