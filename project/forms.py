# students/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Student

class StudentForm(forms.ModelForm):
    # Radio button for matric type (hidden in HTML, handled by JS)
    matric_type = forms.ChoiceField(
        choices=[
            ('single', 'Single Matric'),
            ('double', 'Double Matric'),
        ],
        widget=forms.HiddenInput(),  # Changed to HiddenInput
        initial='single',
        required=True
    )
    
    class Meta:
        model = Student
        fields = ['name', 'old_matric', 'new_matric', 'matric_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'studentName',
                'class': 'form-control',
                'placeholder': ' ',
                'autocomplete': 'off'
            }),
            'old_matric': forms.TextInput(attrs={
                'id': 'oldMatric',
                'class': 'form-control',
                'placeholder': ' ',
                'autocomplete': 'off',
                'oninput': 'formatMatric(this)'
            }),
            'new_matric': forms.TextInput(attrs={
                'id': 'newMatric',
                'class': 'form-control',
                'placeholder': ' ',
                'autocomplete': 'off',
                'oninput': 'formatMatric(this)',
                'disabled': 'disabled'
            }),
            'matric_type': forms.HiddenInput(attrs={
                'id': 'matricTypeField'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom labels and help texts
        self.fields['name'].label = 'Full Name'
        self.fields['old_matric'].label = 'Old Matric Number'
        self.fields['new_matric'].label = 'New Matric Number'
        self.fields['new_matric'].required = False
        
        # If editing, set initial values for JS
        if self.instance and self.instance.pk:
            if self.instance.new_matric:
                self.fields['matric_type'].initial = 'double'
            else:
                self.fields['matric_type'].initial = 'single'
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError("Please enter student name")
        if len(name.strip()) < 2:
            raise ValidationError("Name must be at least 2 characters")
        return name.strip()
    
    def clean_old_matric(self):
        old_matric = self.cleaned_data.get('old_matric')
        if not old_matric:
            raise ValidationError("Old matric number is required")
        
        # Clean the matric number
        old_matric = ''.join(filter(str.isdigit, str(old_matric)))
        
        if not old_matric.startswith(('2024', '2025')):
             raise ValidationError("Matric number must start with 2024 or 2025")

        

        if len(old_matric) < 10:
            raise ValidationError("Matric number must be at least 10 digits")
        
        # Check for duplicates (excluding current student if editing)
        existing = Student.objects.filter(old_matric=old_matric)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise ValidationError(f"Matric number {old_matric} already exists!")
        
        return old_matric
    
    def clean_new_matric(self):
        new_matric = self.cleaned_data.get('new_matric')
        matric_type = self.cleaned_data.get('matric_type')
        
        # If empty string, convert to None
        if not new_matric:
            return None
        
        # Clean the matric number
        new_matric = ''.join(filter(str.isdigit, str(new_matric)))
        
        if not new_matric.startswith(('2024', '2025')):
            raise ValidationError("New matric number must start with 2024 or 2025")
        
        
        if len(new_matric) < 10:
            raise ValidationError("New matric number must be at least 10 digits")
        
        # Check for duplicates (excluding current student if editing)
        existing = Student.objects.filter(new_matric=new_matric)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise ValidationError(f"Matric number {new_matric} already exists!")
        
        # If double matric selected but no new matric
        if matric_type == 'double' and not new_matric:
            raise ValidationError("Please enter new matric number for double matric")
        
        return new_matric
    
    def clean(self):
        cleaned_data = super().clean()
        old_matric = cleaned_data.get('old_matric')
        new_matric = cleaned_data.get('new_matric')
        matric_type = cleaned_data.get('matric_type')
        
        # Validate matric type logic
        if matric_type == 'single' and new_matric:
            raise ValidationError({
                'new_matric': "New matric should be empty for single matric"
            })
        
        if matric_type == 'double' and not new_matric:
            raise ValidationError({
                'new_matric': "Please enter new matric number for double matric"
            })
        
        # Check if old and new are the same
        if new_matric and old_matric == new_matric:
            raise ValidationError({
                'new_matric': "Old and new matric numbers cannot be the same!"
            })
        
        return cleaned_data