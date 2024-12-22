from asgiref.sync import async_to_sync
from django.db.models.signals import post_save  # post_save buradan import edilir
from django.dispatch import receiver
from channels.layers import get_channel_layer  # channels modülü buradan import edilir
from .models import Attendance

@receiver(post_save, sender=Attendance)
def send_late_notification(sender, instance, created, **kwargs):
    if created and instance.late_minutes > 0:
        channel_layer = get_channel_layer()
        message = (
            f"Çalışan {instance.employee.first_name} {instance.employee.last_name}, "
            f"{instance.date.strftime('%Y-%m-%d')} tarihinde işe geç kalmıştır. "
            f"Geç kalma süresi: {instance.late_minutes} dakika."
        )
        async_to_sync(channel_layer.group_send)(
            'admins_notifications',
            {
                'type': 'send_notification',
                'message': message,
            }
        )
