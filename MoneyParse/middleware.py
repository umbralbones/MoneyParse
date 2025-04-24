from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone
from django.conf import settings
import datetime

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            
            if last_activity:
                last_activity_time = datetime.datetime.fromisoformat(last_activity)
                
                if (timezone.now() - last_activity_time).seconds > settings.SESSION_COOKIE_AGE:
                    logout(request)
                    return redirect(settings.LOGIN_URL)
            
            request.session['last_activity'] = timezone.now().isoformat()

        response = self.get_response(request)
        return response
