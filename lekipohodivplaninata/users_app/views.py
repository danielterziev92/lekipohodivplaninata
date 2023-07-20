from django.contrib.auth import views as auth_view, login, get_user_model, mixins, tokens
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import generic as views

from lekipohodivplaninata import settings
from lekipohodivplaninata.core.tasks import send_reset_password_user_email
from lekipohodivplaninata.users_app.forms import SignInForm, SignUpFormUser, UserResetPasswordForm, \
    UserSetPasswordForm, GuideProfileFormUser, BaseUserUpdateForm
from lekipohodivplaninata.core.mixins import UserFormMixin
from lekipohodivplaninata.users_app.models import BaseProfile

UserModel = get_user_model()


class SignInView(auth_view.LoginView):
    authentication_form = SignInForm
    template_name = 'users/sing-in.html'
    success_url = reverse_lazy('index')


class SignUpView(views.CreateView):
    template_name = 'users/sign-up.html'
    form_class = SignUpFormUser
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)
        return result


class SignOutView(auth_view.LogoutView):
    template_name = 'users/logout.html'


class UserDetailView(UserFormMixin, mixins.LoginRequiredMixin, views.DetailView):
    template_name = 'users/detail-user.html'
    success_url = reverse_lazy('user-detail')

    @property
    def model(self):
        return self.get_model()


class UserUpdateInformation(UserFormMixin, mixins.LoginRequiredMixin, views.UpdateView):
    template_name = 'users/edit-user.html'

    def get_success_url(self):
        return reverse_lazy('user-detail', kwargs={
            'pk': self.request.user.pk,
        })

    def get_form_class(self):
        if self.request.user.is_staff:
            return GuideProfileFormUser

        return BaseUserUpdateForm

    @property
    def model(self):
        return self.get_model()

    @property
    def fields(self):
        return self.get_fields_form('first_name', 'last_name')


class UserDeleteView(UserFormMixin, mixins.LoginRequiredMixin, views.DeleteView):
    template_name = 'users/delete-user.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        pk = self.object.pk
        super().form_valid(form)

        if self.request.user.is_staff:
            BaseProfile.objects.get(pk=pk).delete()

        UserModel.objects.get(pk=pk).delete()
        return HttpResponseRedirect(self.success_url)

    @property
    def model(self):
        return self.get_model()


class UserPasswordResetView(auth_view.PasswordResetView):
    template_name = 'users/reset-password.html'
    form_class = UserResetPasswordForm
    success_url = reverse_lazy('reset-password-done')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        associated_user = UserModel.objects.get(email=email)

        send_reset_password_user_email.delay(
            associated_user.pk,
            uid=urlsafe_base64_encode(force_bytes(associated_user.pk)),
            token=tokens.PasswordResetTokenGenerator().make_token(associated_user),
            ip_address=self.request.environ['REMOTE_ADDR'],
            protocol='https' if self.request.is_secure() else 'http',
        )

        cache.set(email, True, timeout=settings.PASSWORD_RESET_TIMEOUT)

        return HttpResponseRedirect(self.get_success_url())


class UserPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = 'users/reset-password-done.html'


class UserPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'users/reset-password-confirm.html'
    post_reset_login = True
    form_class = UserSetPasswordForm
    success_url = reverse_lazy('index')
