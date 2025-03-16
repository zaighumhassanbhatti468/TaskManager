from django.urls import path
from django.contrib.auth import views as auth_views
from core.views.auth_views import login_view,logout_view,profile_view,password_change
from core.views.dashboard_views import admin_dashboard, user_dashboard
from core.views.user_views import manage_users, add_user, update_user, delete_user,toggle_user_status
from core.views.project_views import manage_projects, add_project, update_project, delete_project,get_tasks
from core.views.task_views import manage_tasks, add_task, update_task, delete_task, change_task_priority, reassign_task, user_tasks

urlpatterns = [
    # Login & Register
    path('', login_view, name='login'),  # Default page is the login page
    path('profile/', profile_view, name='profile'),
    path('password_change/', password_change, name='password_change'),
    path('logout/', logout_view, name='logout'),

    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('manage-users/', manage_users, name='manage_users'),
    path('add-user/', add_user, name='add_user'),
    path('update-user/<int:user_id>/', update_user, name='update_user'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path("toggle_user_status/<int:user_id>/", toggle_user_status, name="toggle_user_status"),
    path('get-tasks/<int:project_id>/', get_tasks, name='get_tasks'),

    path('projects/', manage_projects, name='manage_projects'),
    path('projects/add/', add_project, name='add_project'),
    path('projects/update/<int:project_id>/', update_project, name='update_project'),
    path('projects/delete/<int:project_id>/', delete_project, name='delete_project'),

    path('tasks/', manage_tasks, name='manage_tasks'),  # View all tasks
    path('tasks/add/', add_task, name='add_task'),  # Add a new task
    path('tasks/update/<int:task_id>/', update_task, name='update_task'),  # Update task
    path('tasks/delete/<int:task_id>/', delete_task, name='delete_task'),  # Delete task
    path('tasks/change-priority/<int:task_id>/', change_task_priority, name='change_priority'),  # Change priority
    path('tasks/reassign/<int:task_id>/', reassign_task, name='reassign_task'),  # Reassign task
    
    path('dashboard/user/', user_dashboard, name='user_dashboard'),
    path('tasks/my/', user_tasks, name='user_tasks'),
]
