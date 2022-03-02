from django import template


register = template.Library()


def work_exists(base, student):
    return base.works.filter(sender=student).exists()


register.filter('work_exists', work_exists)
