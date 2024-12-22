# utils.py
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
@database_sync_to_async
def send_notification_to_group(message):
    """
    Bu fonksiyon, verilen mesajı WebSocket kanal grubuna gönderir.
    """
    channel_layer = get_channel_layer()
    group_name = 'admins_notifications'
    
    # Mesajı kanala gönder
    channel_layer.group_send(
        group_name,
        {
            'type': 'send_notification',
            'message': message
        }
    )


def process_late_minutes(employee, late_minutes):
    """
    Çalışanın geç kalma süresine göre yıllık izin günlerinden kesinti yapar.
    """
    if late_minutes > 0:  # Geç kalma varsa
        late_days = late_minutes / (8 * 60)  # 1 iş günü = 8 saat
        employee.annual_leave_days -= late_days
        employee.annual_leave_days = max(employee.annual_leave_days, 0)  
        employee.save()