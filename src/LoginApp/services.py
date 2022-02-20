from .models import KvantUser


def isUserExists(user_id):
    """ Проверяет существование пользователя с id - user_id """
    return KvantUser.objects.filter(id=user_id).exists()


def getUserById(id):
    """ 
    Получает пользователя по данному id.
    Если пользователь не существует, возвращает None
    """
    if isUserExists(id):
        return KvantUser.objects.get(id=id)
    return None