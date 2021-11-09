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


register.filter('is_image', is_image)
register.filter('is_files_image', is_files_image)
