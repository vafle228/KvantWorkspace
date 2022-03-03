from django import template
from AdminApp.services import getCourseQuery


register = template.Library()

register.filter('get_user_courses', getCourseQuery)
