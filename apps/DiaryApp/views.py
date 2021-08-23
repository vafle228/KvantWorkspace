from LoginApp.models import KvantUser
from django.shortcuts import render, redirect
from AdminModule.models import KvantLesson, KvantCourse


def diary_page(request, identifier):
    # if not is_available(request, identifier):
    #     return redirect('/login/')

    user = KvantUser.objects.filter(id=identifier)[0]
    if user.permission == 'Ученик':
        course = KvantCourse.objects.filter(students__student=user)[0]
    else:
        course = KvantCourse.objects.filter(teacher__teacher=user)[0]

    lessons = KvantLesson.objects.filter(course=course)
    return render(request, 'DiaryPage/index.html', {'lessons': lessons})
