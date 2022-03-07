from abc import abstractmethod
from django.http import JsonResponse
from django.forms.utils import ErrorDict
from .objects import CreateOrUpdateObject


def getMonthName(month_num):
    """ Получает название месяца по month_num """
    return {
        '01': 'Январь',     '07': 'Июль',
        '02': 'Февраль',    '08': 'Август',
        '03': 'Март',       '09': 'Сентябрь',
        '04': 'Апрель',     '10': 'Октябрь',
        '05': 'Май',        '11': 'Ноябрь',
        '06': 'Июнь',       '12': 'Декабрь',  
    }.get(month_num.zfill(2))

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
    return f'{date.year}-{str(date.month).zfill(2)}-{str(date.day).zfill(2)}'


class ObjectManipulationResponse:
    """ Генерирует JsonResponse на ajax запрос """
    def getResponse(self, obj_or_errors):
        """ Генерирует ответ основываясь на newsOrError объекте """
        if isinstance(obj_or_errors, ErrorDict):
            return JsonResponse({'status': 400, 'errors': obj_or_errors})
        return JsonResponse({'status': 200, 'link': self._constructRedirectUrl(obj_or_errors)})
    
    @abstractmethod
    def _constructRedirectUrl(self, obj):
        """ Генерирует редирект ссылку """
        raise NotImplementedError


class ObjectManipulationManager(ObjectManipulationResponse, CreateOrUpdateObject):
    def updateObject(self, request):
        obj_or_errors = self._getUpdatedObject(request)
        return self.getResponse(obj_or_errors)
    
    def _getUpdatedObject(self, request):
        return super().updateObject(request)
    
    def createObject(self, request):
        obj_or_errors = self._getCreatedObject(request)
        return self.getResponse(obj_or_errors)
    
    def _getCreatedObject(self, request):
        return super().createObject(request)