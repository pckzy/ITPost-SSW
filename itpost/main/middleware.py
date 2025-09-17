from django.shortcuts import redirect

class SessionAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = ['/login', '/register', '/admin', '/static']

        if not request.session.get('user_id') and not any(request.path.startswith(path) for path in allowed_paths):
            return redirect('/login')

        response = self.get_response(request)
        return response
