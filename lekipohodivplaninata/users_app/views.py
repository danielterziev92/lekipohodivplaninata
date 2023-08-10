from django.contrib.auth import views as auth_view, login, get_user_model, mixins, tokens
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
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




