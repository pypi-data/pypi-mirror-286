from django.shortcuts import redirect
from django.urls import reverse_lazy
from authX.authX_settings import AUTHX_SETTINGS

class LoginRequiredMixin:
    redirect_url = reverse_lazy(AUTHX_SETTINGS['AUTHX_LOGIN_URL'])

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)

class RedirectIfAuthenticatedMixin:
    redirect_url = reverse_lazy(AUTHX_SETTINGS['AUTHX_DASHBOARD_URL'])

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)