from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import Group, Permission
from personal_track.models import Employee  # Modelinize uygun olarak değiştirin

class Command(BaseCommand):
    help = 'Rastgele çalışan verisi oluşturur'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Group ve Permission'ları alalım (isteğe bağlı)
        groups = Group.objects.all()
        permissions = Permission.objects.all()

        for _ in range(500):  # 10 adet çalışan ekler
            # Çalışan oluştur
            first_name = fake.first_name()
            last_name = fake.last_name()

            employee = Employee.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=f"{first_name}{last_name}",  # Kullanıcı adı oluşturuldu
                password='Serkan159.',  # Güçlü bir parola kullanılabilir
                role=fake.random_element(elements=('Employee', 'Manager')),
                annual_leave_days=15,  # Yıllık izin günleri
                date_joined=fake.date_this_decade(),  # İşe başlama tarihi
                phone_number=fake.phone_number(),
                address=fake.address(),
                is_active=fake.boolean(),
                card_number=fake.unique.random_number(digits=5),  # Kart numarası
            )

            # Rastgele Group ve Permission ekleyelim
            if groups:
                employee.groups.add(fake.random_element(groups))
            if permissions:
                employee.user_permissions.add(fake.random_element(permissions))

            self.stdout.write(self.style.SUCCESS(f'Çalışan oluşturuldu: {employee.first_name} {employee.last_name}'))
