from django.urls import path

from lekipohodivplaninata.users_app.views import SignInView, UsersListView, SignUpView, SignOutView

urlpatterns = (
    path('', UsersListView.as_view(), name='all users'),
    path('sign-in/', SignInView.as_view(), name='sign in user'),
    path('sign-up/', SignUpView.as_view(), name='sign up user'),
    path('sign-out', SignOutView.as_view(), name='sign out user'),
)
