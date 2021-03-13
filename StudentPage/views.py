from django.shortcuts import render


def main_page(request):
    return render(request, 'StudentPage/MainPage/index.html')


def dairy_page(request):
    return render(request, 'StudentPage/DiaryPage/index.html')


def mail_page(request):
    return render(request, 'StudentPage/MailPage/index.html')


def statistics_page(request):
    return render(request, 'StudentPage/StatisticsPage/index.html')
