from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    # Ana sayfa ve çalışanlarla ilgili sayfalar
    path('', views.home, name="home"),
    path('employees/', views.employees, name="employees"),
    path('employee_list/', views.EmployeeListView.as_view(), name='employee_list'),
    path('add_employee/', views.add_employee, name='add_employee'),
    
    # Giriş / Çıkış sayfaları
    path('login/', views.login, name='login'),
    path('personal/login/', views.personal_login, name='personal_login'),
    path('personal/logout/', views.personal_logout, name='personal_logout'),
    path('manager/login/', views.manager_login, name='manager_login'),
    path('manager/logout/', views.manager_logout, name='manager_logout'),
    
    # Çalışan izinleri ve devamsızlıkla ilgili sayfalar
    path('employee/<int:id>/info/', views.personal_info, name='personal_info'),
    path('personal_leaves', views.personal_leaves, name='personal_leaves'),
    path('apply_for_leave/', views.apply_for_leave, name='apply_for_leave'),
    path('update_leave_status/<int:leave_id>/', views.update_leave_status, name='update_leave_status'),
    path('attendance_status/', views.attendance_status, name="attendance_status"),
    path('leave_create/', views.leave_create, name="leave_create"),
    path('back_to_work', views.back_to_work, name='back_to_work'),
    path('total_work_hours', views.total_work_hours, name='total_work_hours'),
    path('daily_attendance', views.daily_attendance, name='daily_attendance'),
    # API'ler
    path('api/card-check/', views.card_check, name='card_check'),
    path('api/daily-attendance/', views.daily_attendance_api, name='daily-attendance-api'),


    # Çıkış işlemleri
    path('personal_logout/', views.personal_logout, name="personal_logout"),
    path('manager_logout/', views.manager_logout, name="manager_logout")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
