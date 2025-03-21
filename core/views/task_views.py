from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from core.models import Task, Project, User, Comment
from datetime import date, timedelta
from datetime import datetime

@login_required
def manage_tasks(request):
    """View for listing all tasks."""
    if request.user.is_superuser:
        tasks = Task.objects.all()
        projects = Project.objects.all()
        users = User.objects.filter(is_superuser=False)
    else:
        tasks = Task.objects.filter(assigned_to=request.user)
        projects = Project.objects.filter(task__assigned_to=request.user).distinct()
        users = User.objects.none()
    
    today = date.today()
    tomorrow = today + timedelta(days=1)
    return render(request, 'core/manage_tasks.html', {
        'tasks': tasks,
        'projects': projects,
        'users': users,
        'today': today,
        'tomorrow': tomorrow
    })

@login_required
@csrf_exempt
def add_task(request):
    """View for adding a new task."""
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority', 'Medium')
        status = request.POST.get('status', 'Not Started')

        project_id = request.POST.get('project')
        assigned_to_id = request.POST.get('assigned_to')
        project = get_object_or_404(Project, id=int(project_id))
        assigned_to = get_object_or_404(User, id=int(assigned_to_id))

        task = Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            project=project,
            assigned_to=assigned_to,
            priority=priority,
            status=status
        )

        return JsonResponse({'success': 'Task added successfully', 'task_id': task.id})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def update_task(request, task_id):
    """View for updating a task."""
    task = get_object_or_404(Task, id=task_id)

    # Only the superuser or the assigned user can update the task
    if not request.user.is_superuser and request.user != task.assigned_to:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == "POST":
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)

        # Ensure the due date is converted to a proper date object
        due_date_str = request.POST.get('due_date')
        if due_date_str:
            task.due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()

        task.priority = request.POST.get('priority', task.priority)
        task.status = request.POST.get('status', task.status)

        # Update project if provided
        project_id = request.POST.get('project')
        if project_id:
            task.project = get_object_or_404(Project, id=int(project_id))

        # Update assigned user if provided
        assigned_to_id = request.POST.get('assigned_to')
        if assigned_to_id:
            task.assigned_to = get_object_or_404(User, id=int(assigned_to_id))

        # Save the updated task
        task.save()

        return JsonResponse({'success': 'Task updated successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def delete_task(request, task_id):
    """View for deleting a task."""
    task = get_object_or_404(Task, id=task_id)

    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    task.delete()
    return JsonResponse({'success': 'Task deleted successfully'})

@login_required
@csrf_exempt
def change_task_priority(request, task_id):
    """View for changing a task's priority."""
    task = get_object_or_404(Task, id=task_id)

    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == "POST":
        new_priority = request.POST.get('priority')
        if new_priority:
            task.priority = new_priority
            task.save()
            return JsonResponse({'success': 'Task priority updated'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def reassign_task(request, task_id):
    """View for reassigning a task to a different user."""
    task = get_object_or_404(Task, id=task_id)

    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == "POST":
        new_user_id = request.POST.get('new_user_id')
        new_user = get_object_or_404(User, id=new_user_id)
        task.assigned_to = new_user
        task.save()
        return JsonResponse({'success': 'Task reassigned successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def user_tasks(request):
    """View for a user to see their assigned tasks."""
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'core/user_tasks.html', {'tasks': tasks})


@login_required
def get_task_comments(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    comments = Comment.objects.filter(task=task, parent__isnull=True).order_by("-created_at")  # Only fetch parent comments

    def serialize_comment(comment):
        """Recursively serialize a comment along with its replies"""
        return {
            "id": comment.id,
            "user": "You" if comment.user == request.user else comment.user.fullname,
            "content": comment.content,
            "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
            "is_owner": comment.user == request.user,
            "replies": [serialize_comment(reply) for reply in comment.replies.all().order_by("created_at")]  # Get replies sorted by date
        }

    comments_data = [serialize_comment(comment) for comment in comments]
    
    return JsonResponse({"comments": comments_data})



@csrf_exempt
@login_required
def add_comment(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        comment_text = request.POST.get("comment_text")

        if not task_id or not comment_text:  # Ensure task_id is valid
            return JsonResponse({"success": False, "error": "Missing task_id or comment_text"}, status=400)

        task = get_object_or_404(Task, id=task_id)
        comment = Comment.objects.create(task=task, user=request.user, content=comment_text)

        
        return JsonResponse({"success": True, "comment_id": comment.id})
    
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


@csrf_exempt
@login_required
def add_reply(request):
    if request.method == "POST":
        comment_id = request.POST.get("comment_id")
        reply_text = request.POST.get("reply_text")

        if not comment_id or not reply_text:  # Ensure comment_id is valid
            return JsonResponse({"success": False, "error": "Missing comment_id or reply_text"}, status=400)

        parent_comment = get_object_or_404(Comment, id=comment_id)

        reply = Comment.objects.create(
            task=parent_comment.task,
            user=request.user,
            content=reply_text,
            parent=parent_comment
        )

        return JsonResponse({"success": True, "reply_id": reply.id})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

