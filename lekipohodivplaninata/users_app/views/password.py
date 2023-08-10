from django.conf import settings
from django.contrib.auth import views as auth_view, tokens, get_user_model
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from lekipohodivplaninata.users_app.forms import UserResetPasswordForm, UserSetPasswordForm
from lekipohodivplaninata.core.tasks import send_reset_password_user_email

UserModel = get_user_model()


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
