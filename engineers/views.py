from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Engineer


@login_required
def engineer_list_view(request):
    if request.user.role != 'ADMIN':
        engineers = Engineer.objects.none()
    else:
        engineers = Engineer.objects.all()

    return render(request, 'engineers/engineer_list.html', {
        'engineers': engineers
    })