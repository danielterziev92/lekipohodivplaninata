from django.urls import include
from django.urls import path

from lekipohodivplaninata.users_app.views import SignInView, SignUpView, SignOutView, \
    UserPasswordResetView, UserPasswordResetDoneView, UserPasswordResetConfirmView, \
    UserDetailView, UserUpdateInformation, UserDeleteView

urlpatterns = (
    path('sign-in', SignInView.as_view(), name='sign in user'),
    path('sign-up', SignUpView.as_view(), name='sign up user'),
    path('sign-out', SignOutView.as_view(), name='sign out user'),
    path('reset-password', include([
        path('', UserPasswordResetView.as_view(), name='reset password'),
        path('/password-reset/done', UserPasswordResetDoneView.as_view(), name='reset password done'),
        path('/password-reset/<uidb64>/<token>', UserPasswordResetConfirmView.as_view(), name='reset password confirm'),
    ])),
    path('<int:pk>', include([
        path('', UserDetailView.as_view(), name='user detail'),
        path('/edit', UserUpdateInformation.as_view(), name='user edit'),
        path('/delete', UserDeleteView.as_view(), name='user delete'),
    ])),
)
