from LoginPage.views import is_available
from django.shortcuts import render, redirect


def dairy_page(request, identifier):
    if not is_available(request, identifier):
        return redirect('/auth/')

    return render(request, 'StudentPage/DiaryPage/index.html')


def mail_page(request, identifier):
    return render(request, 'StudentPage/MailPage/index.html')


def statistics_page(request, identifier):
    if not is_available(request, identifier):
        return redirect('/auth/')
    return render(request, 'StudentPage/StatisticsPage/index.html')
