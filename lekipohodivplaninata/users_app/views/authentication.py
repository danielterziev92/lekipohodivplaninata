from django.contrib import messages
from django.contrib.auth import views as auth_view, login
from django.views import generic as views
from django.urls import reverse_lazy

from lekipohodivplaninata.users_app.forms import SignInForm, SignUpFormUser


class SignInView(auth_view.LoginView):
    authentication_form = SignInForm
    template_name = 'users/sing-in.html'

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, 'Успешно влязохте в профила си.')
        return result


class SignUpView(views.CreateView):
    template_name = 'users/sign-up.html'
    form_class = SignUpFormUser
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form._request = self.request
        result = super().form_valid(form)

        login(self.request, self.object)
        return result


class SignOutView(auth_view.LogoutView):
    template_name = 'users/logout.html'
