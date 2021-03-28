from django.shortcuts import render
from GeneralPage.models import KvantNews


def main_page(request, identifier):
    return render(request, 'StudentPage/MainPage/index.html')


def dairy_page(request, identifier):
    return render(request, 'StudentPage/DiaryPage/index.html')


def mail_page(request, identifier):
    return render(request, 'StudentPage/MailPage/index.html')


def statistics_page(request, identifier):
    return render(request, 'StudentPage/StatisticsPage/index.html')
