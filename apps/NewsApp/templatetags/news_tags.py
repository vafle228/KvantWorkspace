from django import template

register = template.Library()


def file_extension(file):
    return file.file.name.split(".")[-1]


def file_name(file):
    return file.file.name.split("/")[-1]


def get_objects(model_object):
    return model_object.all()


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
register.filter('file_name', file_name)
register.filter('get_objects', get_objects)
register.filter('file_extension', file_extension)
register.filter('is_files_image', is_files_image)
