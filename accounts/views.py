from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')