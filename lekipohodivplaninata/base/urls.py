from django.urls import path, include

from lekipohodivplaninata.base.views import IndexListView, UpcomingEventListView, PassedEventListView, SignUpHike, \
    SiteEvaluationView, SignedForHikeListView

urlpatterns = (
    path('', IndexListView.as_view(), name='index'),
    path('upcoming/', UpcomingEventListView.as_view(), name='hikes upcoming'),
    path('passed/', PassedEventListView.as_view(), name='hikes passed'),
    path('<int:pk>/<slug:slug>/', include([
        path('sign-up/', SignUpHike.as_view(), name='sign up for hike'),
        path('all-recorded/', SignedForHikeListView.as_view(), name='all signed for hike')
    ])),
    path('site-evaluation/', SiteEvaluationView.as_view(), name='site evaluation')
)

from .signals import *
