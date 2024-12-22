from .models import Leave
from django.utils.timezone import now
def pending_leave_requests(request):
    # Bekleyen izin taleplerini al
    total_leave_request = Leave.objects.filter(status='pending').count()
    return {
        'total_leave_request': total_leave_request
    }
def today(request):
    today = now().date()
    return {
        'today': today
    }