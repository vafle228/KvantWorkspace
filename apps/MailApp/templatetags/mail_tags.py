from django import template

register = template.Library()

def get_active_btn(current_type, btn_type):
    return 'active' if current_type == btn_type else ''

register.filter('get_active_btn', get_active_btn)
