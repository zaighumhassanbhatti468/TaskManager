from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from core.models import Project
from core.models import Task

@login_required
def manage_projects(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    projects = Project.objects.all()
    return render(request, 'core/manage_projects.html', {'projects': projects})

@login_required
@csrf_exempt
def add_project(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')

        if Project.objects.filter(name=name).exists():
            return JsonResponse({'error': 'Project with this name already exists'}, status=400)

        project = Project.objects.create(name=name, description=description)
        return JsonResponse({'success': 'Project added successfully', 'project_id': project.id})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def update_project(request, project_id):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        project.name = request.POST.get('name', project.name)
        project.description = request.POST.get('description', project.description)
        project.save()
        return JsonResponse({'success': 'Project updated successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def delete_project(request, project_id):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return JsonResponse({'success': 'Project deleted successfully'})

@login_required
@csrf_exempt
def get_tasks(request, project_id):
    tasks = Task.objects.filter(project_id=project_id).values(
        "title", "description", "status", "priority", "assigned_to__fullname"
    )
    return JsonResponse({"tasks": list(tasks)})