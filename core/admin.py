from django.contrib import admin
from core.models import User, Role, Project, Task, TaskPriority, TaskStatus

# Register User Model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", "phonenumber", "role")
    search_fields = ("fullname", "email", "phonenumber")
    list_filter = ("role",)

# Register Other Models
admin.site.register(Role)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TaskPriority)
admin.site.register(TaskStatus)
