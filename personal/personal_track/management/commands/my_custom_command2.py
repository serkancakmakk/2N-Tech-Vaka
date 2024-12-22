from django.core.management.base import BaseCommand
from faker import Faker
from personal_track.models import Employee, Attendance
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Çalışanlar için sahte yoklama (attendance) verileri oluşturur.'

    def handle(self, *args, **kwargs):
        fake = Faker()
        employees = Employee.objects.all()  # Sistemdeki tüm çalışanları al
        if not employees.exists():
            self.stdout.write(self.style.ERROR("Hiç çalışan bulunamadı. Lütfen önce çalışan oluşturun!"))
            return

        for employee in employees:
            for _ in range(1):  # Her çalışan için 5 günlük sahte yoklama oluştur
                # Rastgele bir tarih oluştur
                date = fake.date_between(start_date='-30d', end_date='today')  # Son 30 gün
                check_in_hour = random.randint(8, 10)  # 08:00 ile 10:00 arasında giriş
                check_in_minute = random.randint(0, 59)
                check_out_hour = random.randint(16, 18)  # 16:00 ile 18:00 arasında çıkış
                check_out_minute = random.randint(0, 59)

                # Giriş ve çıkış saatlerini oluştur
                check_in = datetime.combine(date, datetime.min.time()) + timedelta(hours=check_in_hour, minutes=check_in_minute)
                check_out = datetime.combine(date, datetime.min.time()) + timedelta(hours=check_out_hour, minutes=check_out_minute)

                # Geç kalma süresini hesapla (örnek: 09:00 iş başlangıç saati)
                scheduled_start_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=9)
                late_minutes = max(0, int((check_in - scheduled_start_time).total_seconds() // 60))

                # Çalışılan saatleri hesapla
                worked_hours = (check_out - check_in).total_seconds() / 3600

                # Attendance kaydı oluştur
                attendance = Attendance.objects.create(
                    employee=employee,
                    date=date,
                    check_in=check_in,
                    check_out=check_out,
                    late_minutes=late_minutes,
                    worked_hours=worked_hours
                )

                self.stdout.write(self.style.SUCCESS(f'{employee.first_name} {employee.last_name} için yoklama oluşturuldu: {date}'))
