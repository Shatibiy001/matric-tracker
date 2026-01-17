# students/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Add student
    path('add/', views.add_student, name='add_student'),
    
    # View single matric students
    path('single/', views.single_matric, name='single_matric'),
    
    # View double matric students
    path('double/', views.double_matric, name='double_matric'),
    
    # Edit student
    #path('edit/<int:student_id>/', views.edit_student, name='edit_student'),
    
    # Delete student
    #path('delete/<int:student_id>/', views.delete_student, name='delete_student'),
    
    # Search
    path('search/', views.search_student, name='search_student'),
]