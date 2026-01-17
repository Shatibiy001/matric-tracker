# students/models.py
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    
    # All students have old matric
    old_matric = models.CharField(max_length=20, unique=True)
    
    # Some have new matric (optional)
    new_matric = models.CharField(max_length=20, blank=True, null=True, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.old_matric}"
    
    def has_double_matric(self):
        return bool(self.new_matric)