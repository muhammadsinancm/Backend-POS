from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUsezrAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("POS Information", {"fields": ("role")}))