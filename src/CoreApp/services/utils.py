from abc import abstractmethod
from django.http import JsonResponse
from django.forms.utils import ErrorDict


def getSizeWithSuffix(nbytes):
    """ Возвращает значение nbytes в максимально возможных единицах """
    suffix_index = 0
    suffixes = ['B', 'kB', 'mB', 'gB', 'tB', 'pB']
    
    while nbytes >= 1024 and suffix_index < len(suffixes) - 1:
        nbytes /= 1024.
        suffix_index += 1
    size = ('%.2f' % nbytes).split(".00")[0]

    return f'{size}{suffixes[suffix_index]}'


def buildDate(date):
    """ Генерация строки даты, для пути сохранения файлов """
    return f'{date.year}-{str(date.month).zfill(2)}-{date.day}'


class ObjectManupulationResponse:
    """ Генерирует JsonResponse на ajax запрос """
    def getResponse(self, request, obj_or_errors):
        """ Генерирует ответ основываясь на newsOrError объекте """
        if isinstance(obj_or_errors, ErrorDict):
            return JsonResponse({'status': 400, 'errors': obj_or_errors})
        return JsonResponse({'status': 200, 'link': self._constructRedirectUrl(request, obj_or_errors)})
    
    @abstractmethod
    def _getRedirectKwargs(self, request, obj=None):
        """ Генерирует аргументы для редирект ссылки """
        raise NotImplementedError
    
    @abstractmethod
    def _constructRedirectUrl(self, request, obj=None):
        """ Генерирует редирект ссылку """
        raise NotImplementedError