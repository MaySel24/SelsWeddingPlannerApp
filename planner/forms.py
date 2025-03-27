from datetime import date
from django import forms
from django.contrib.auth.models import User
from .models import Guest, Task, Vendor, Budget, WeddingColor, Profile, TotalBudget

# ========================= LOGIN FORM =========================
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
# ========================= GUEST FORM =========================
class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['name', 'email', 'phone', 'rsvp_status', 'table_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Guest Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'rsvp_status': forms.Select(attrs={'class': 'form-control'}),
            'table_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Table Number'}),
        }


# ========================= TASK FORM =========================
class TaskForm(forms.ModelForm):
    assigned_to = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
        label="Assign To"
    )  # Now a text field instead of a dropdown

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter task details', 'rows': 3}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < date.today():
            raise forms.ValidationError("Due date cannot be in the past.")
        return due_date


# ========================= VENDOR FORM =========================
class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'service_type', 'phone', 'email', 'contract_signed', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vendor Name'}),
            'service_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service Type'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'contract_signed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional Notes', 'rows': 3}),
        }


# ========================= BUDGET FORM =========================
class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount_allocated', 'amount_spent']

# ========================= TOTAL BUDGET FORM =========================
class TotalBudgetForm(forms.ModelForm):
    class Meta:
        model = TotalBudget
        fields = ['amount']

# ========================= WEDDING COLOR FORM =========================
class WeddingColorForm(forms.ModelForm):
    class Meta:
        model = WeddingColor
        fields = ['name', 'hex_code']
        widgets = {
            'hex_code': forms.TextInput(attrs={'type': 'color'}),  # Color picker
        }

# ========================= PROFILE FORM =========================
class TaglineForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['tagline']