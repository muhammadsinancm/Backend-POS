from django.contrib import admin

from .models import Table

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("id","number","capacity","status","is_active",)
    list_filter = ("status", "is_active")
    search_fields = ("number",)
