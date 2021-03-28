from django import template

register = template.Library()


def file_extension(file):
    return file.file.name.split(".")[-1]


def file_name(file):
    return file.file.name.split("/")[-1]


def get_files(files):
    return files.all()


register.filter('file_name', file_name)
register.filter('get_files', get_files)
register.filter('file_extension', file_extension)
