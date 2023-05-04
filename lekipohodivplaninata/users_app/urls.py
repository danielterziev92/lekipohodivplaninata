from django.urls import path

from lekipohodivplaninata.users_app.views import SignInView, UsersListView, SignUpView, SignOutView, \
    UserPasswordResetView, UserPasswordResetDoneView, UserPasswordResetConfirmView, UserPasswordResetCompleteView

urlpatterns = (
    path('', UsersListView.as_view(), name='all users'),
    path('sign-in/', SignInView.as_view(), name='sign in user'),
    path('sign-up/', SignUpView.as_view(), name='sign up user'),
    path('sign-out', SignOutView.as_view(), name='sign out user'),
    path('password-reset/', UserPasswordResetView.as_view(), name='reset password'),
    path('password-reset/done/', UserPasswordResetDoneView.as_view(), name='reset password done'),
    path('password-reset/<uidb64>/<token>', UserPasswordResetConfirmView.as_view(), name='reset password confirm'),
    path('password-reset/complete', UserPasswordResetCompleteView.as_view(), name='reset password complete'),

)
