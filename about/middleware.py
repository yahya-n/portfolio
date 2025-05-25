# about/middleware.py - FIXED VERSION
from django.utils.timezone import now
from .models import Metrics
from django.conf import settings

class UserSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip tracking for admin pages, static files, and API endpoints
        skip_paths = ['/admin/', '/track-event/', settings.STATIC_URL, settings.MEDIA_URL]
        
        if any(request.path.startswith(path) for path in skip_paths):
            return self.get_response(request)
            
        response = self.get_response(request)
        
        # Only track GET requests for main pages
        if request.method == 'GET' and hasattr(request, 'session'):
            try:
                if not request.session.session_key:
                    request.session.create()
                
                # Track page view
                Metrics.objects.create(
                    event_type='page_view',
                    session_key=request.session.session_key,
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    path=request.path
                )
                
                print(f"Page view tracked: {request.path}")  # Debug line
                
                # Update session info
                request.session['last_activity'] = now().isoformat()
                request.session.set_expiry(3600)  # 1 hour
                
            except Exception as e:
                print(f"Error in middleware: {e}")  # Debug line
            
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip