from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .utils import process_late_minutes, send_notification_to_group
from django.http import JsonResponse
from django.views.generic import View
from .models import Employee
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from .models import Attendance, Employee, Attendance, Employee, CompanySettings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import make_aware, now
from .serializers import AttendanceSerializer
from .models import Employee, Attendance
from django.db.models import Sum
from django.db import models
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Q
from django.views import View
from .forms import EmployeeCreationForm
from django.contrib import messages


def home(request):
    user = request.user
    leaves = []  # Başlangıçta boş bir liste
    employees_with_less_than_3_days_left = Employee.objects.filter(
        annual_leave_days__lte=3
    )
    if user.role == "Employee":
        leaves = Leave.objects.filter(employee=user)
        context = {"user": user, "leaves": leaves}  # Sayfa objesini context'e ekle

        return render(request, "home.html", context)
    elif user.role == "Manager":
        total_employee = Employee.objects.filter(is_active=True)
        total_leave_request = Leave.objects.filter(status="pending")
        leaves = Leave.objects.all()  # Tüm izin taleplerini getir

    # Sayfalama işlemi
    paginator = Paginator(leaves, 5)  # Sayfa başına 5 izin başvurusu göster
    page_number = request.GET.get("page")  # Sayfa numarasını URL parametresinden al
    page_obj = paginator.get_page(page_number)  # Sayfa objesini oluştur

    context = {
        "employees_with_less_than_3_days_left": employees_with_less_than_3_days_left,
        "total_leave_request": total_leave_request,
        "total_employee": total_employee,
        "user": user,
        "page_obj": page_obj,  # Sayfa objesini context'e ekle
    }

    return render(request, "home.html", context)


@login_required
def employees(request):
    employees = Employee.objects.filter(is_active=True)
    context = {
        "employees": employees,
    }
    return render(request, "employees.html", context)


class EmployeeListView(View):
    def get(self, request, *args, **kwargs):
        # Başlangıç ve uzunluk parametrelerini al
        start = int(request.GET.get("start", 0))  # Sayfa başı
        length = int(request.GET.get("length", 10))  # Sayfa uzunluğu
        search_value = request.GET.get("search[value]", "")  # Arama değeri
        order_column = request.GET.get("order[0][column]", "0")  # Sıralama kolonu
        order_dir = request.GET.get("order[0][dir]", "asc")  # Sıralama yönü
        status = request.GET.get("status", "active")  # 'active' veya 'inactive'

        # Duruma göre filtreleme (aktif veya pasif çalışanlar)
        if status == "active":
            queryset = Employee.objects.filter(is_active=True)
        else:
            queryset = Employee.objects.filter(is_active=False)

        # Arama işlemi
        if search_value:
            queryset = queryset.filter(
                Q(first_name__icontains=search_value)
                | Q(last_name__icontains=search_value)
                | Q(phone_number__icontains=search_value)
                | Q(role__icontains=search_value)
            )

        # Sıralama işlemi
        order_field = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "date_joined",
            "address",
            "card_number",
        ][int(order_column)]
        if order_dir == "desc":
            queryset = queryset.order_by(f"-{order_field}")
        else:
            queryset = queryset.order_by(order_field)

        # Sayfalama
        employees = queryset[start : start + length]

        # Veriyi hazırlama
        data = []
        for employee in employees:
            data.append(
                {
                    "id": employee.id,
                    "full_name": f"{employee.first_name} {employee.last_name}",
                    "phone_number": employee.phone_number,
                    "role": employee.role,
                    "date_joined": employee.date_joined.strftime("%Y-%m-%d"),
                    "address": employee.address,
                    "card_number": employee.card_number,
                }
            )

        # Toplam çalışan sayısını döndürme (sayfalama için)
        total_records = Employee.objects.count()
        filtered_records = queryset.count()

        return JsonResponse(
            {
                "draw": request.GET.get("draw"),
                "recordsTotal": total_records,
                "recordsFiltered": filtered_records,
                "data": data,
            }
        )


@login_required
def add_employee(request):
    if request.method != "POST":
        form = EmployeeCreationForm()
        return render(request, "add_employee.html", {"form": form})

    form = EmployeeCreationForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, "Hesabınız başarıyla oluşturuldu!")
        return redirect("add_employee")

    # Hataları formun içinde tutarak onları template'e gönderiyoruz
    for field in form:
        for error in field.errors:
            messages.error(request, f"{field.label}: {error}")

    return render(request, "add_employee.html", {"form": form})


@api_view(["POST"])
def card_check(request):
    """
    Kart okuma işlemi yapan API.
    Bu API, gönderilen kart numarasına göre çalışanın giriş ve çıkış saatlerini alır ve ilgili işlemleri yapar.

    API kullanımı:
    Kullanıcı bir kart numarası gönderir ve API, bu kart numarasına karşılık gelen çalışanın
    günlük giriş çıkış saatlerini kontrol eder.
    Eğer giriş yapılmamışsa, giriş kaydı oluşturur ve geç giriş durumunda bildirim gönderir.
    Eğer çıkış yapılmamışsa, çıkış kaydını oluşturur.

    API Yolu:
        POST http://127.0.0.1:8000/api/card-check/

    Gönderilecek JSON Verisi:
        {
            "card_number": "1234"   # Çalışanın kart numarası
        }

    Başarılı Yanıt:
        Giriş veya çıkış saati kaydedildiği, geç giriş varsa bildirim gönderildiği hakkında bilgi içerir.

    Hata Yanıtı:
        - Kart numarası verilmemişse hata döner.
        - Çalışan aktif değilse hata döner.
        - Tatil gününde kart okuma yapılmak istenirse hata döner.
    """
    card_number = request.data.get("card_number")

    if not card_number:
        return Response(
            {
                "error": "Kart numarası gereklidir!",
                "status": "error",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    employee = get_object_or_404(Employee, card_number=card_number)

    if not employee.is_active:
        return Response(
            {
                "message": "Kullanıcı aktif değil.",
                "status": "error",
            }
        )

    today = timezone.localdate()  # Bugünün tarihi, yerel saate göre alınıyor
    company_settings = CompanySettings.objects.first()

    # Tatil günlerini kontrol et
    if company_settings and today.strftime("%A") in company_settings.holidays:
        return Response(
            {
                "message": "Bugün tatil günü, kart okuma işlemi yapılamaz.",
                "status": "error",
            }
        )

    # Çalışma başlangıç saati
    work_start_time = (
        company_settings.work_start_time
        if company_settings
        else datetime.min.time().replace(hour=8, minute=0)
    )
    expected_start_time = make_aware(datetime.combine(today, work_start_time))

    # Attendance kaydını oluştur veya getir
    attendance, created = Attendance.objects.get_or_create(
        employee=employee,
        date=today,
        defaults={
            "check_in": None,
            "check_out": None,
            "late_minutes": 0,
            "worked_hours": 0.0,
        },
    )

    if created:
        # Giriş kaydını yap
        attendance.check_in = timezone.now()  # Yerel saate göre şu anki zamanı al
        check_in_time = attendance.check_in

        if check_in_time > expected_start_time:
            attendance.late_minutes = (
                check_in_time - expected_start_time
            ).seconds // 60
        else:
            attendance.late_minutes = 0

        attendance.save()

        # Geç giriş olduğunu tespit et ve WebSocket ile bildirim gönder ve yıllık izinden düş.
        if attendance.late_minutes > 0:
            process_late_minutes(employee, attendance.late_minutes)
            message = f"{employee.first_name} {employee.last_name} geç giriş yaptı. Saat: {attendance.check_in.strftime('%H:%M:%S')}"
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "admins_notifications",
                {"type": "send_notification", "message": message},
            )

        return Response(
            {
                "message": f'Giriş saati kaydedildi. Çalışan ID: {employee.id}, Çalışan: {employee.first_name} {employee.last_name}, Saat: {attendance.check_in.strftime("%H:%M:%S")}',
                "late_minutes": attendance.late_minutes,
                "attendance": AttendanceSerializer(attendance).data,
                "status": "success",
            }
        )
    else:
        if attendance.check_in and not attendance.check_out:
            # Çıkış kaydını yap
            attendance.check_out = timezone.now()  # Yerel saate göre çıkış zamanını al
            check_in_time = attendance.check_in
            check_out_time = attendance.check_out
            attendance.worked_hours = (check_out_time - check_in_time).seconds / 3600.0
            attendance.save()
            return Response(
                {
                    "message": f'Çıkış saati kaydedildi. Çalışan ID: {employee.id}, Çalışan: {employee.first_name} {employee.last_name}, Saat: {attendance.check_out.strftime("%H:%M:%S")}',
                    "late_minutes": attendance.late_minutes,
                    "attendance": AttendanceSerializer(attendance).data,
                    "status": "success",
                }
            )
        else:
            return Response(
                {
                    "error": "Geçerli bir giriş kaydı bulunmuyor!",
                    "status": "error",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


@login_required
def total_work_hours(request):
    # Varsayılan olarak şu anki ay ve yıl
    selected_year = request.GET.get("year", datetime.now().year)
    selected_month = request.GET.get("month", datetime.now().month)

    # Filtrelenmiş veriler
    employees = Employee.objects.annotate(
        total_work_hours=Sum(
            "attendance_records__worked_hours",
            filter=(
                models.Q(attendance_records__date__year=selected_year)
                & models.Q(attendance_records__date__month=selected_month)
            ),
        )
    )

    context = {
        "employees": employees,
        "selected_year": selected_year,
        "selected_month": selected_month,
    }
    return render(request, "total_work_hours.html", context)


def daily_attendance(request):
    """
    Belirli bir tarihteki giriş/çıkışların listelendiği sayfa.
    """
    # Tarih parametresini al, yoksa bugünün tarihi kullan
    date_str = request.GET.get('date', now().date().strftime('%Y-%m-%d'))
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        selected_date = now().date()  # Geçersiz tarih gönderilirse bugüne dön
    
    # Seçilen tarihe göre filtrele
    daily_attendance = Attendance.objects.filter(date=selected_date)
    
    context = {
        "daily_attendance": daily_attendance,
        "selected_date": selected_date,  # Seçilen tarihi şablona gönder
    }
    return render(request, "daily_attendance.html", context)

@api_view(["GET"])
def daily_attendance_api(request):
    """
    Günlük giriş/çıkış verilerini JSON formatında döner.
    Tüm çalışanların giriş/çıkış verilerini gösterir.
    """

    today = now().date()
    attendances = Attendance.objects.filter(date=today).select_related("employee")
    employees = Employee.objects.filter(is_active=True)

    data = []
    for employee in employees:
        attendance = attendances.filter(employee=employee).first()

        if attendance:
            check_in = (
                attendance.check_in.strftime("%H:%M:%S")
                if attendance.check_in
                else "N/A"
            )
            check_out = (
                attendance.check_out.strftime("%H:%M:%S")
                if attendance.check_out
                else "N/A"
            )
            late_minutes = attendance.late_minutes
            worked_hours = round(attendance.worked_hours, 2)
        else:
            check_in = "N/A"
            check_out = "N/A"
            late_minutes = 0
            worked_hours = 0.0

        data.append(
            {
                "employee_name": f"{employee.first_name} {employee.last_name}",
                "date": today.strftime("%Y-%m-%d"),
                "check_in": check_in,
                "check_out": check_out,
                "late_minutes": late_minutes,
                "worked_hours": worked_hours,
            }
        )

    return JsonResponse(data, safe=False)


def back_to_work(request):
    """
    Kart Okuma Sayfası
    """
    return render(request, "back_to_work.html")


# Personel Login
def personal_login(request):
    """
    Personel için login
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Geçersiz kimlik bilgileri.")
    return render(request, "login/personal_login.html")


# Manager Login
def manager_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role == "Manager":  # Role kontrolü
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Geçersiz kimlik bilgileri veya yetki yok.")
    return render(request, "login/manager_login.html")


def personal_logout(request):
    logout(request)
    return redirect("personal_login")


def manager_logout(request):
    logout(request)
    return redirect("manager_login")


def personal_leaves(request):
    employee = Employee.objects.get(id=request.user.id)
    total_leave_days = Leave.objects.filter(employee=employee, status="approved")
    context = {}
    return render(
        request,
        "personal_leaves.html",
        {
            "total_leave_days": total_leave_days,
            "annual_leave_days": employee.annual_leave_days,
            
        },
    )


# İzin başvurusu yapma
def apply_for_leave(request):
    """
    Çalışan izin başvurusunu alır ve toplam izin gününü hesaplar.
    """
    leave_type = None
    start_date = None
    end_date = None
    total_days = None

    if request.method == "POST":
        # Formdan gelen verileri alıyoruz
        leave_type = request.POST.get("leave_type")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        # Başvuru tarihleri ve izin türü üzerinde doğrulama yapıyoruz
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            if start_date > end_date:
                messages.error(
                    request, "Başlangıç tarihi bitiş tarihinden sonra olamaz."
                )
                return redirect("apply_for_leave")

            # İzin başvurusu oluşturuluyor
            leave = Leave.objects.create(
                employee=request.user,  # Veya geçerli kullanıcı
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                total_days=(end_date - start_date).days + 1,
                created_by=request.user,
            )
            total_days = (end_date - start_date).days + 1
            leave.save()
            messages.success(
                request,
                f"İzin başvurunuz başarıyla alındı! Toplam {total_days} gün izin talep ettiniz.",
            )
            return redirect("home")  # Başka bir sayfaya yönlendirme yapabilirsiniz

        except ValueError:
            messages.error(request, "Geçersiz tarih formatı.")
            return redirect("apply_for_leave")

    return render(
        request,
        "personal_leaves.html",
        {
            "leave_type": leave_type,
            "start_date": start_date,
            "end_date": end_date,
            "total_days": total_days,
        },
    )


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


def update_leave_status(request, leave_id):
    """
    İzin başvurusunun durumunu günceller.
    """
    if request.method == "POST":
        leave = get_object_or_404(Leave, id=leave_id)
        new_status = request.POST.get("status")

        # Durum değerini kontrol et ve güncelle
        if new_status in ["approved", "pending", "rejected"]:
            # Eğer onaylanırsa çalışan izin günlerini düşür
            if new_status == "approved":
                if leave.employee.annual_leave_days > 0:
                    leave.employee.annual_leave_days -= 1.0
                    leave.employee.save()  # Çalışanın güncel durumunu kaydet
                else:
                    messages.error(request, "Çalışanın yeterli izin günü yok.")
                    return redirect("home")

            leave.status = new_status
            leave.save()  # İzin durumunu kaydet
            messages.success(request, "İzin durumu başarıyla güncellendi.")
        else:
            messages.error(request, "Geçersiz durum seçildi.")

    return redirect("home")


from django.shortcuts import render
from django.utils.timezone import now
from .models import Attendance, Leave, Employee


def attendance_status(request):
    # Bugünün tarihini al
    today = now().date()

    # Attendance kaydı olan çalışanların ID'lerini al
    attended_employee_ids = Attendance.objects.filter(date=today).values_list(
        "employee_id", flat=True
    )

    # Attendance kaydı olmayan çalışanları al
    missing_check_ins = Employee.objects.exclude(id__in=attended_employee_ids)

    # Bugün izinli olanlar (onaylanmış izinler)
    approved_leaves = Leave.objects.filter(
        start_date__lte=today, end_date__gte=today, status="approved"
    ).select_related("employee")

    # Verileri şablona gönder
    context = {
        "missing_check_ins": missing_check_ins,
        "approved_leaves": approved_leaves,
    }
    return render(request, "attendance_status.html", context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Leave, Employee
from .forms import LeaveForm


def leave_create(request):
    """
    Yetkilinin izin tanımlama sayfaası
    """
    if not request.user.role == "Manager":
        messages.success(request, "Bu alana erişemezsiniz")
        return redirect("home")  # Başarılı işleme yönlendirme
    employees = Employee.objects.all()  # Çalışanları listele
    leave_types = Leave.LEAVE_TYPE_CHOICES  # İzin türlerini al

    if request.method == "POST":
        form = LeaveForm(request.POST)

        if form.is_valid():
            # Başlangıç ve bitiş tarihlerini al
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]

            # Tarihler arasındaki farkı hesapla
            if start_date and end_date:
                delta = end_date - start_date
                total_days = delta.days + 1  # 1 ekliyoruz çünkü her iki gün de dahil

                # Formu kaydetmeden önce total_days'i atıyoruz
                leave = form.save(commit=False)
                leave.total_days = total_days
                leave.status = "approved"
                leave.created_by = request.user
                leave.save()

                # Başarılı kaydetme işlemi
                messages.success(request, "İzin talebiniz başarıyla oluşturuldu.")
                return redirect("leave_create")  # Başarılı işleme yönlendirme
            else:
                messages.error(
                    request, "Başlangıç ve bitiş tarihleri doğru girilmelidir."
                )
        else:
            messages.error(request, "Formda hata var.")

    else:
        form = LeaveForm()

    context = {
        "form": form,
        "employees": employees,
        "leave_types": leave_types,  # İzin türlerini şablona gönder
    }

    return render(request, "leave_create.html", context)


from django.shortcuts import get_object_or_404, render
from .models import Employee, Leave


def personal_info(request, id):
    # Çalışanı al
    personal = get_object_or_404(Employee, id=id)

    # Onaylanmış izinleri al
    approved_leaves = Leave.objects.filter(employee=personal, status="approved")

    context = {
        "personal": personal,
        "approved_leaves": approved_leaves,
    }
    return render(request, "personal_info.html", context)
