from django.contrib.auth import views as auth_view, login, get_user_model, mixins
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic as views

from lekipohodivplaninata.users_app.forms import SignInForm, SignUpForm, UserResetPasswordForm, UserSetPasswordForm, \
    GuideProfileForm
from lekipohodivplaninata.users_app.mixins import UserFormMixin
from lekipohodivplaninata.users_app.models import BaseProfile, GuideProfile

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


class UserDetailView(UserFormMixin, mixins.LoginRequiredMixin, views.DetailView):
    template_name = 'users/detail-user.html'
    success_url = reverse_lazy('user detail')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        if self.object.pk != request.user.pk:
            raise Http404

        return super().get(request, *args, **kwargs)

    @property
    def model(self):
        return self.get_model_form()


class UserUpdateInformation(UserFormMixin, mixins.LoginRequiredMixin, views.UpdateView):
    template_name = 'users/edit-user.html'

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('user detail', kwargs={
            'pk': self.request.user.pk,
        })

    @property
    def model(self):
        return self.get_model_form()

    @property
    def fields(self):
        return self.get_fields_form('first_name', 'last_name')

    @property
    def form_class(self):
        return self.get_form_clas_form()


class UserDeleteView(mixins.LoginRequiredMixin, views.DeleteView):
    template_name = 'users/delete-user.html'
    model = BaseProfile
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        super().form_valid(form)
        self.request.user.delete()
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        if self.object.pk != request.user.pk:
            raise Http404

        return super().get(request, *args, **kwargs)


class UserPasswordResetView(auth_view.PasswordResetView):
    template_name = 'users/reset-password.html'
    form_class = UserResetPasswordForm
    from_email = 'Леки походи в планината <support@lekipohodivplaninata.bg>'
    email_template_name = 'users/email-templates/reset-password.html'
    subject_template_name = 'users/email-templates/password_reset_subject.txt'
    success_url = reverse_lazy('reset password done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.title = 'Забравена парола'
        return context


class UserPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = 'users/reset-password-done.html'


class UserPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'users/reset-password-confirm.html'
    post_reset_login = True
    form_class = UserSetPasswordForm
    success_url = reverse_lazy('index')
