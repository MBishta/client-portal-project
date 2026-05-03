from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EngineerForm
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


@login_required
def engineer_detail_view(request, pk):
    if request.user.role != 'ADMIN':
        engineer = None
        projects = []
    else:
        engineer = get_object_or_404(Engineer, pk=pk)
        projects = engineer.projects.all()

    return render(request, 'engineers/engineer_detail.html', {
        'engineer': engineer,
        'projects': projects,
    })


@login_required
def engineer_create_view(request):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = EngineerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('engineers:engineer_list')
    else:
        form = EngineerForm()

    return render(request, 'engineers/engineer_form.html', {
        'form': form,
        'page_title': 'Add Engineer',
        'button_text': 'Save Engineer',
    })


@login_required
def engineer_edit_view(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    engineer = get_object_or_404(Engineer, pk=pk)

    if request.method == 'POST':
        form = EngineerForm(request.POST, instance=engineer)

        if form.is_valid():
            form.save()
            return redirect('engineers:engineer_detail', pk=engineer.pk)
    else:
        form = EngineerForm(instance=engineer)

    return render(request, 'engineers/engineer_form.html', {
        'form': form,
        'page_title': 'Edit Engineer',
        'button_text': 'Save Changes',
    })


@login_required
def engineer_delete_view(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('accounts:dashboard')

    engineer = get_object_or_404(Engineer, pk=pk)

    if request.method == 'POST':
        engineer.delete()
        return redirect('engineers:engineer_list')

    return redirect('engineers:engineer_detail', pk=engineer.pk)