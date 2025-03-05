from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import User, Project, Task
from django.views.decorators.cache import never_cache

@never_cache
@login_required
def admin_dashboard(request):
    """View for superadmin dashboard"""
    print("Admin dashboard view is being executed")  # Add this line
    if not request.user.is_superuser:
        print("User is not a superuser")  # Add this line
        return render(request, 'core/403.html', status=403)
    total_users = User.objects.count()
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()
    total_completed_tasks = Task.objects.filter(status='Completed').count()
    total_not_started_tasks = Task.objects.filter(status='Not Started').count()
    total_in_progress_tasks = Task.objects.filter(status='In Progress').count()
    total_on_hold_tasks = Task.objects.filter(status='On Hold').count()
    context = {
        'total_users': total_users,
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'total_completed_tasks': total_completed_tasks,
        'total_not_started_tasks': total_not_started_tasks,
        'total_in_progress_tasks': total_in_progress_tasks,
        'total_on_hold_tasks': total_on_hold_tasks,
    }
    return render(request, 'core/admin_dashboard.html', context)

@login_required
def user_dashboard(request):
    """View for user dashboard"""
    total_tasks = Task.objects.filter(assigned_to=request.user).count()
    total_projects = Project.objects.filter(task__assigned_to=request.user).distinct().count()
    total_completed_tasks = Task.objects.filter(assigned_to=request.user, status='Completed').count()
    total_not_started_tasks = Task.objects.filter(assigned_to=request.user, status='Not Started').count()
    total_in_progress_tasks = Task.objects.filter(assigned_to=request.user, status='In Progress').count()
    total_on_hold_tasks = Task.objects.filter(assigned_to=request.user, status='On Hold').count()

    context = {
        'total_tasks': total_tasks,
        'total_projects': total_projects,
        'total_completed_tasks': total_completed_tasks,
        'total_not_started_tasks': total_not_started_tasks,
        'total_in_progress_tasks': total_in_progress_tasks,
        'total_on_hold_tasks': total_on_hold_tasks,
    }
    return render(request, 'core/user_dashboard.html', context)
