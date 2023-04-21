from django.urls import path

from lekipohodivplaninata.users_app.views import UsersListView

urlpatterns = (
    path('', UsersListView.as_view(), name='all users'),
)
