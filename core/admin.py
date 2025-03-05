from django.contrib import admin
from core.models import User, Project, Task

# Register User Model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", "phonenumber")
    search_fields = ("fullname", "email", "phonenumber")

# Register Other Models
admin.site.register(Project)
admin.site.register(Task)
