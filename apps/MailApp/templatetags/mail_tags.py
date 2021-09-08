from django import template

register = template.Library()


def file_extension(file):
    return file.file.name.split(".")[-1]


def file_name(file):
    return file.file.name.split("/")[-1]


def get_objects(model_object):
    return model_object.all()


def get_active_btn(current_type, btn_type):
    return 'active' if current_type == btn_type else ''


register.filter('file_name', file_name)
register.filter('get_objects', get_objects)
register.filter('file_extension', file_extension)
register.filter('get_active_btn', get_active_btn)
