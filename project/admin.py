# students/admin.py
from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'old_matric', 'new_matric', 'matric_type', 'created_at']
    search_fields = ['name', 'old_matric', 'new_matric']
    list_filter = ['created_at']
    
    def matric_type(self, obj):
        if obj.new_matric:
            return "Double"
        return "Single"
    matric_type.short_description = 'Type'