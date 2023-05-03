from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_view, login, authenticate
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib import messages

from lekipohodivplaninata.users_app.forms import SignInForm, SignUpForm

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
