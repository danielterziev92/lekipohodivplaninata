from django.urls import path

from lekipohodivplaninata.users_app.views import SignInView, UsersListView

urlpatterns = (
    path('', UsersListView.as_view(), name='all users'),
    path('login/', SignInView.as_view(), name='login user')
)
