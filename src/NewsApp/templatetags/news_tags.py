from django import template


register = template.Library()


def _get_file_type(file):
    return file.file.file.obj.content_type


def is_image(file):
    return _get_file_type(file).split('/')[0] == 'image'


def is_files_image(files):
    for file in files:
        if is_image(file):
            return True
    return False


def get_active_shedule(course, day):
    if course.schedule.filter(week_day=day).exists():
        return course.schedule.get(week_day=day)
    return None


register.filter('is_image', is_image)
register.filter('is_files_image', is_files_image)
register.filter('get_active_shedule', get_active_shedule)


