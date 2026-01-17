# students/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Student
from .forms import StudentForm
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import StudentForm



def home(request):
    """Home page showing all students"""
    students = Student.objects.all().order_by('-created_at')
    
    # Get counts
    total = Student.objects.count()
    single = Student.objects.filter(new_matric__isnull=True).count()
    double = Student.objects.filter(new_matric__isnull=False).count()
    
    context = {
        'students': students,
        'total': total,
        'single': single,
        'double': double,
    }
    return render(request, 'project/home.html', context)



def add_student(request):
    """Handle student registration with AJAX support"""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if form.is_valid():
                student = form.save()
                return JsonResponse({
                    'success': True,
                    'message': f'Student {student.name} registered successfully!',
                    'student_id': student.id,
                    'student': {
                        'name': student.name,
                        'old_matric': student.old_matric,
                        'new_matric': student.new_matric or '',
                        'matric_type': 'double' if student.new_matric else 'single'
                    }
                })
            else:
                # Return form errors as JSON
                errors = {}
                for field, error_list in form.errors.items():
                    errors[field] = error_list[0] if error_list else ''
                
                return JsonResponse({
                    'success': False,
                    'errors': errors,
                    'message': 'Please correct the errors below.'
                }, status=400)
        
        # Regular form submission (non-AJAX)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.name} registered successfully!')
            return redirect('home')
    
    else:
        form = StudentForm()
    
    context = {
        'form': form,
        'title': 'Register Student',
    }
    return render(request, 'project/add_student.html', context)

# AJAX endpoint to check matric number availability
@csrf_exempt
def check_matric_availability(request):
    """Check if matric number already exists"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            matric_number = data.get('matric_number', '')
            matric_type = data.get('matric_type', 'old')  # 'old' or 'new'
            
            if not matric_number:
                return JsonResponse({'available': False, 'error': 'Matric number required'})
            
            # Clean the matric number
            matric_number = ''.join(filter(str.isdigit, str(matric_number)))
            
            # Check in database
            if matric_type == 'old':
                exists = Student.objects.filter(old_matric=matric_number).exists()
            else:
                exists = Student.objects.filter(new_matric=matric_number).exists()
            
            return JsonResponse({
                'available': not exists,
                'matric_number': matric_number,
                'message': 'Matric number already exists!' if exists else 'Matric number available'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def single_matric(request):
    """Show students with single matric only"""
    students = Student.objects.filter(new_matric__isnull=True).order_by('name')
    
    context = {
        'students': students,
    }
    return render(request, 'project/single_matric.html', context)

def double_matric(request):
    """Show students with double matric only"""
    students = Student.objects.filter(new_matric__isnull=False).order_by('name')
    
    context = {
        'students': students,
    }
    return render(request, 'project/double_matric.html', context)



def search_student(request):
    """Search students by name or matric"""
    query = request.GET.get('q', '')
    students = []
    
    if query:
        students = Student.objects.filter(
            Q(name__icontains=query) |
            Q(old_matric__icontains=query) |
            Q(new_matric__icontains=query)
        ).order_by('name')
    
    context = {
        'students': students,
        'query': query,
        'has_results': bool(students)
    }
    return render(request, 'project/search_results.html', context)