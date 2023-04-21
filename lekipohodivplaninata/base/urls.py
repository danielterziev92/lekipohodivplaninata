from django.urls import path

from lekipohodivplaninata.base.views import IndexPageTemplateView

urlpatterns = (
    path('', IndexPageTemplateView.as_view(), name='index'),
)
