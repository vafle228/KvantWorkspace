import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import re


def validate_snils(value):
    pattern = re.compile('([0-9]{3})-([0-9]{3})-([0-9]{3}) ([0-9]{2})')
    if pattern.match(value) is None:
        raise ValidationError(_('Некорректный номер снилс'))


def validate_telephone(value):
    num_pattern, plus_pattern = re.compile('([0-9]+)'), re.compile('[+]([0-9]+)')
    if num_pattern.match(value) is None and plus_pattern.match(value) is None:
        raise ValidationError(_('Укажите номер телефона без пробелов и прочих спец символов'))


def validate_date(value):
    try:
        datetime.datetime.strptime(value, '%d.%m.%Y')
    except ValueError:
        raise ValidationError(_('Укажите дату в формате дд.мм.гггг или проверьте ее правильность'))
