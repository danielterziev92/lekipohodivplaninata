from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_form
from django.contrib.auth import views as auth_view
from django.views import generic as views

UserModel = get_user_model()


class SignInView(auth_view.LoginView):
    template_name = 'accounts/login-page.html'


class SignUpForm(auth_form.UserCreationForm):
    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD,)
        field_classes = {}


class UsersListView(views.ListView):
    model = UserModel
    template_name = 'users/index.html'
