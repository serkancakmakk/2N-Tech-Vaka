

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Employee(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(
        max_length=50, choices=[('Employee', 'Employee'), ('Manager', 'Manager')]
    )
    annual_leave_days = models.FloatField(default=15.0)  # Yıllık izin günleri
    date_joined = models.DateField(auto_now_add=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    card_number = models.CharField(unique=True,max_length=255,null=True,blank=True) # Giriş Çıkışları kartlı sistemde düşündüm.
    # related_name ile çakışma engelleniyor
    groups = models.ManyToManyField(
        Group,
        related_name='employee_groups',  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='employee_permissions',  
        blank=True
    )

    class Meta:
        db_table = 'Employee'

    def __str__(self):
        return self.first_name + self.last_name

from django.db import models
from django.utils import timezone

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField(auto_now_add=True)
    check_in = models.DateTimeField(null=True, blank=True, db_index=True)

    check_out = models.DateTimeField(null=True, blank=True, db_index=True)  # Daha önce timestamp olabilirdi
    late_minutes = models.IntegerField(default=0)  # Geç kalma süresi dakika cinsinden
    worked_hours = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.employee.first_name + self.employee.last_name} - {self.date}"

    class Meta:
        db_table = 'Attendance'

class Notification(models.Model):
    recipient = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.first_name + self.recipient.last_name } - Read: {self.is_read}"
    class Meta:
        db_table = 'Notification'
from django.db import models

class CompanySettings(models.Model):
    work_start_time = models.TimeField(default="08:00:00")
    work_end_time = models.TimeField(default="18:00:00")
    holidays = models.JSONField(default=["Saturday", "Sunday"])  # Varsayılan olarak Cumartesi ve Pazar


    def __str__(self):
        return "Company Settings"

    class Meta:
        db_table = 'CompanySettings'
# izin modeli
class Leave(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('sick', 'Sick Leave'),
        ('vacation', 'Vacation'),
        ('personal', 'Personal Leave'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Çalışan ile ilişkilendir
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)  # İzin türü
    start_date = models.DateField()  # İzin başlangıç tarihi
    end_date = models.DateField()  # İzin bitiş tarihi
    total_days = models.FloatField()  # İzin gün sayısı
    status = models.CharField(max_length=20, default='pending', choices=[('approved', 'Approved'), ('pending', 'Pending'), ('rejected', 'Rejected')])  # Onay durumu
    reason = models.TextField(null=True, blank=True)  # İzin nedeni (isteğe bağlı)
    created_by = models.ForeignKey(Employee, related_name='created_leaves', on_delete=models.CASCADE)  # İzin talebini oluşturan çalışan

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.leave_type} ({self.start_date} to {self.end_date})"
    def get_status_display(self):
        return dict([('approved', 'Approved'), ('pending', 'Pending'), ('rejected', 'Rejected')]).get(self.status, 'Unknown')
    class Meta:
        ordering = ['-start_date']  # Son izin önce gelsin
        db_table = 'Leave'
        