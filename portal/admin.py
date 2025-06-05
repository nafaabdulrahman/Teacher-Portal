from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Add the custom fields to the admin form
    fieldsets = UserAdmin.fieldsets + (
        ("Security Info", {"fields": ("security_question", "security_answer")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Security Info", {"fields": ("security_question", "security_answer")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
