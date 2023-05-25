from django.urls import path

from lekipohodivplaninata.base.views import IndexPageTemplateView, SignUpHike

urlpatterns = (
    path('', IndexPageTemplateView.as_view(), name='index'),
    path('<int:pk>/<slug:slug>/sign-up', SignUpHike.as_view(), name='sign up for hike')
)
