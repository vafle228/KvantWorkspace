from django import template


def getFileExtension(file):
    return file.file.name.split(".")[-1]


def getFileName(file):
    return file.file.name.split("/")[-1]


def getObjects(model_object):
    return model_object.all()


def getActiveBtn(active, aside):
    return "active" if aside == active else ""


def getFileSize(file):
    suffix_index = 0
    nbytes = file.file.size
    suffixes = ['B', 'kB', 'MB', 'GB', 'TB', 'PB']
    
    while nbytes >= 1024 and suffix_index < len(suffixes) - 1:
        nbytes /= 1024.
        suffix_index += 1
    size = ('%.2f' % nbytes).split(".00")[0]

    return f'{size} {suffixes[suffix_index]}'


def getText(html):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html)


register = template.Library()

register.filter('get_text', getText)
register.filter('get_objects', getObjects)
register.filter('get_file_size', getFileSize)
register.filter('get_file_name', getFileName)
register.filter('get_active_btn', getActiveBtn)
register.filter('get_file_extension', getFileExtension)
