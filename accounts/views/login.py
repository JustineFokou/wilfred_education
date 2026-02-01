# accounts/views/login.py
from django.urls import reverse
from django.contrib.auth.views import LoginView, LogoutView


class CustomLoginView(LoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return reverse("admin:dashboard")
        return super().get_success_url()


class CustomLogoutView(LogoutView):
    pass
