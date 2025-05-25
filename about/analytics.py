from django.utils.timezone import now, timedelta
from .models import Metrics

def track_event(event_type, request=None):
    """Track a user interaction event"""
    session_key = request.session.session_key if request and hasattr(request, 'session') else None
    ip_address = request.META.get('REMOTE_ADDR') if request else None
    
    Metrics.objects.create(
        event_type=event_type,
        session_key=session_key,
        ip_address=ip_address,
    )