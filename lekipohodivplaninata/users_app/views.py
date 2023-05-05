from django.contrib.auth import views as auth_view, login, get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views

from lekipohodivplaninata.users_app.forms import SignInForm, SignUpForm, UserResetPasswordForm

UserModel = get_user_model()


class SignInView(auth_view.LoginView):
    authentication_form = SignInForm
    template_name = 'users/sing-in.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('index')


class SignUpView(views.CreateView):
    template_name = 'users/sign-up.html'
    form_class = SignUpForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)
        return result


class SignOutView(auth_view.LogoutView):
    template_name = 'users/logout.html'


class UsersListView(views.ListView):
    model = UserModel
    template_name = 'users/all-users.html'


class UserPasswordResetView(auth_view.PasswordResetView):
    template_name = 'users/reset-password.html'
    form_class = UserResetPasswordForm
    from_email = 'Леки походи в планината <support@lekipohodivplaninata.bg>'
    email_template_name = 'users/email-template/reset-password.html'
    success_url = reverse_lazy('reset password done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.title = 'Забравена на парола'
        return context


class UserPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = 'users/reset-password-done.html'


class UserPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'users/reset-password-confirm.html'


class UserPasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = 'users/reset-password-complete.html'
