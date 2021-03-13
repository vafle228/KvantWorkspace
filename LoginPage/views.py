from .forms import KvantUserLoginForm
from django.shortcuts import render, redirect


def login_page(request):
    return render(request, 'LoginPage/index.html')


def login_user(request):
    user = None
    if request.method == 'POST':
        form = KvantUserLoginForm(request.POST)
        user = form.save(request) if form.is_valid() else None
    return redirect('/auth/' if user is None else
                    '/student/' if user.permission == 'Ученик' else
                    '/teacher/' if user.permission == 'Учитель' else '/administration/')
