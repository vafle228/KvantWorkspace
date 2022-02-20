from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class LoginAppTemplateView(LoginView):
    """ Контроллер авторизации на странице """
    template_name = 'LoginApp/index.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка авторизации!')
        return super().form_invalid(form)
    
    def get_success_url(self):
        redirect_kwargs = {
            'identifier': self.request.user.id}
        return reverse_lazy('main_page', kwargs=redirect_kwargs)
