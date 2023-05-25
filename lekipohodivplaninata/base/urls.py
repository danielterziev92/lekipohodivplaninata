from django.urls import path

from lekipohodivplaninata.base.views import IndexPageTemplateView, SignUpHike

urlpatterns = (
    path('', IndexPageTemplateView.as_view(), name='index'),
    path('sign-up-for-hike/<int:pk>/<slug:slug>', SignUpHike.as_view(), name='sign up for hike')
)
