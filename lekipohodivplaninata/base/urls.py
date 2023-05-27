from django.urls import path

from lekipohodivplaninata.base.views import IndexListView, UpcomingEventListView, PassedEventListView, SignUpHike

urlpatterns = (
    path('', IndexListView.as_view(), name='index'),
    path('upcoming', UpcomingEventListView.as_view(), name='hikes upcoming'),
    path('passed', PassedEventListView.as_view(), name='hikes passed'),
    path('<int:pk>/<slug:slug>/sign-up', SignUpHike.as_view(), name='sign up for hike')
)
