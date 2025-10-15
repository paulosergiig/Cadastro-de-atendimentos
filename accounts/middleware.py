from django.shortcuts import redirect
from django.urls import reverse

class PasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'therapist_profile'):
            if request.user.therapist_profile.must_change_password:
                # Permite acesso à página de mudança de senha e ao logout
                if request.path not in [reverse('accounts:password_change'), reverse('logout')]:
                    return redirect('accounts:password_change')
        
        response = self.get_response(request)
        return response