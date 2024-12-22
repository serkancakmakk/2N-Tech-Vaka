from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee, Leave

class EmployeeCreationForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ('username', 'first_name', 'last_name', 'role', 'phone_number', 'address', 'card_number', 'password1', 'password2')
class LeaveForm(forms.ModelForm):
    leave_types = Leave.LEAVE_TYPE_CHOICES  # İzin türlerini formda kullanılabilir hale getirme

    class Meta:
        model = Leave
        fields = ['employee', 'leave_type', 'start_date', 'end_date', 'reason']

    leave_type = forms.ChoiceField(choices=leave_types)  # İzin türü için seçim alanı

    # Çalışanları listele
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.filter(is_active=True),  # Sadece aktif çalışanlar
        required=True,
        empty_label="Select Employee"  # "Çalışan Seçin" yazısı
    )