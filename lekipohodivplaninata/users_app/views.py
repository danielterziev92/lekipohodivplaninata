from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_form
from django.views import generic as views

UserModel = get_user_model()


class SignUpForm(auth_form.UserCreationForm):
    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD,)
        field_classes = {}


class UsersListView(views.ListView):
    model = UserModel
    template_name = 'users/index.html'

