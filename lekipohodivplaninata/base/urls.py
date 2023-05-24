from django.urls import path

from lekipohodivplaninata.base.views import IndexPageTemplateView
from lekipohodivplaninata.base.views import SignUpHike

urlpatterns = (
    path('', IndexPageTemplateView.as_view(), name='index'),
    path('sign-up-for-hike', SignUpHike.as_view(), name='sign-up for hike')
)
