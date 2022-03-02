from django import template


register = template.Library()


def get_mark(base, user): 
    return base.marks.get(student=user).mark if has_mark(base, user) else ''


def has_mark(base, student):
    return base.marks.filter(student=student).exists()


def get_mark_class(base, user):
    query = {
        '1': 'mark poor',   '4': 'mark excellent',
        '2': 'mark badly',  'ОТ': 'mark leave',
        '3': 'mark fine',   'УП': 'mark reason',}
    return query.get(get_mark(base, user)) or ''


def get_avarage_mark(lessons, user):
    val, count = 0, 0
    for lesson in lessons:
        for task in lesson.tasks.all():
            if task.base.marks.filter(student=user).exists():
                count += 1
                val += int(task.base.marks.get(student=user).mark)
    
    return '{:0.2f}'.format(val / count) if count != 0 else '0'


def get_avarage_attendance(lessons, user):
    if len(lessons) == 0: return 0
    
    val = 0
    for lesson in lessons:
        if lesson.base.marks.filter(student=user).exists():
            val += 1 if lesson.base.marks.get(student=user).mark == 'ОТ' else 0
    return f'{int(((len(lessons) - val) / len(lessons)) * 100)}%'


def get_active_mark(mark, seeking):
    return 'active' if seeking == mark else None


register.filter('has_mark', has_mark)
register.filter('get_mark', get_mark)
register.filter('get_mark_class', get_mark_class)
register.filter('get_active_mark', get_active_mark)
register.filter('get_avarage_mark', get_avarage_mark)
register.filter('get_avarage_attendance', get_avarage_attendance)
