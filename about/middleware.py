from django.utils.timezone import now

class UserSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if hasattr(request, 'session'):
            if not request.session.session_key:
                request.session.create()
            request.session['last_activity'] = now().isoformat()
            request.session.set_expiry(300)  # 5 minutes
            
        return response