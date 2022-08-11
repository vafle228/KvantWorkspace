from django.views import generic
from . import services
from LoginApp.forms import KvantUserCreationForm
from django.http import QueryDict


class RegisterPageTemplateView(services.RegistrationAccessMixin, generic.TemplateView):
    template_name = 'RegisterApp/index.html'

    def dispatch(self, request, *args, **kwargs):
        kwargs.update(register_key=request.GET.get('key'))
        return super().dispatch(request, *args, **kwargs)


class UserCreateView(services.RegistrationAccessMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        kwargs.update(register_key=request.POST.get('key'))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        manager = services.UserCreatinManager([KvantUserCreationForm])
        new_post = QueryDict(mutable=True); new_post.update(
            {
                'surname': request.POST.get('surname'),
                'name': request.POST.get('name'),
                'patronymic': request.POST.get('patronymic'),
                'username': request.POST.get('login'),
                'password1': request.POST.get('password1'),
                'password2': request.POST.get('password2'),
                'permission': services.getTempUrlByKey(kwargs.get('register_key')).permission,
            }
        )
        request.POST = new_post; return manager.registerUser(request, kwargs.get('register_key'))
