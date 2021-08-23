from .forms import KvantUserLoginForm
from django.shortcuts import redirect
from django.views.generic import TemplateView, View


# View для отображения страницы авторизации
class LoginPageTemplateView(TemplateView):
    template_name = 'LoginApp/index.html'


class UserLogInView(View):
    def post(self, request, *args, **kwargs):
        from django.urls import reverse_lazy
        
        form = KvantUserLoginForm(request.POST)  # Форма авторизации
        user = form.save(request) if form.is_valid() else None  # Попытка авторизации

        if user is not None:
            return redirect(reverse_lazy('main_page', kwargs={'identifier': user.id}))           
        return redirect(reverse_lazy('login_page'))
