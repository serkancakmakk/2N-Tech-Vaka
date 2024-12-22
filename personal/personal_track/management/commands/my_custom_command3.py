from django.core.management.base import BaseCommand
from faker import Faker
from personal_track.models import Employee, Attendance, Leave
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Rastgele izin verisi oluşturur'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Çalışan listesini al
        employees = Employee.objects.all()

        if not employees.exists():
            self.stdout.write(self.style.ERROR("Hiç çalışan bulunamadı! Önce çalışan verileri oluşturun."))
            return

        LEAVE_TYPES = ['sick', 'vacation', 'personal']
        STATUSES = ['approved', 'pending', 'rejected']

        for _ in range(20):  # 20 adet izin kaydı oluştur
            employee = random.choice(employees)  # Rastgele bir çalışan seç
            leave_type = random.choice(LEAVE_TYPES)
            status = random.choice(STATUSES)

            # Rastgele bir tarih aralığı belirle
            start_date = fake.date_between(start_date='-1y', end_date='today')
            end_date = start_date + timedelta(days=random.randint(1, 10))  # 1 ile 10 gün arasında süre

            # İzin gün sayısını hesapla
            total_days = (end_date - start_date).days + 1

            # İzin kaydı oluştur
            leave = Leave.objects.create(
                employee=employee,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                total_days=total_days,
                status=status,
                reason=fake.sentence(),
                created_by=random.choice(employees)  # Rastgele bir çalışan tarafından oluşturulmuş gibi
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"İzin kaydı oluşturuldu: {leave.employee.first_name} {leave.employee.last_name} - {leave_type} ({leave.start_date} - {leave.end_date})"
                )
            )
