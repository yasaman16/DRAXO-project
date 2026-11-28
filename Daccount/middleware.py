import time

from django.contrib.auth import logout


class SessionIdleTimeoutMiddleware:
    idle_timeout = 3 * 24 * 60 * 60
    activity_key = 'last_authenticated_activity'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Capture activity before the view, which may log the user in or out.
        now = int(time.time())
        if request.user.is_authenticated:
            last_activity = request.session.get(self.activity_key)
            if last_activity is not None and now - last_activity >= self.idle_timeout:
                logout(request)

        response = self.get_response(request)
        if request.user.is_authenticated:
            request.session[self.activity_key] = now
        return response
