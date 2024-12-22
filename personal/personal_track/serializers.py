# serializers.py

from rest_framework import serializers
from .models import Attendance
from .models import Employee  # Employee modelinin doğru şekilde import edildiğinden emin olun

from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name']  # Sadece ihtiyacınız olan alanları seçin

class AttendanceSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()  # Employee bilgilerini serialize etmek için

    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'date', 'check_in', 'check_out', 'late_minutes', 'worked_hours']
