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


def get_news_tag(user):
    return 'Общее'


def get_active_shedule(shedules, day):
    for shedule in shedules:
        if shedule.day == day: return True
    return False


register.filter('is_image', is_image)
register.filter('get_news_tag', get_news_tag)
register.filter('is_files_image', is_files_image)
register.filter('get_active_shedule', get_active_shedule)


