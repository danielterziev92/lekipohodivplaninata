from django.urls import path, include

from lekipohodivplaninata.base.views import IndexListView, UpcomingEventListView, PassedEventListView, SignUpHike, \
    SiteEvaluationView, SignedForHikeListView, SignedForHikeUpdateView, confirm_user_for_hike

urlpatterns = (
    path('', IndexListView.as_view(), name='index'),
    path('upcoming/', UpcomingEventListView.as_view(), name='hikes upcoming'),
    path('passed/', PassedEventListView.as_view(), name='hikes passed'),
    path('recorded/<int:pk>/edit/', SignedForHikeUpdateView.as_view(), name='signed for hike update'),
    path('recorded/<int:pk>/confirmed/<str:text>', confirm_user_for_hike, name='signed for hike confirm'),
    # path('cancel/', confirm_user_for_hike, name='signed for hike cancel'),
    # path('recommend/', ),),
    path('<int:pk>/<slug:slug>/', include([
        path('sign-up/', SignUpHike.as_view(), name='sign up for hike'),
        path('all-recorded/', SignedForHikeListView.as_view(), name='all signed for hike')
    ])),
    path('site-evaluation/', SiteEvaluationView.as_view(), name='site evaluation')
)

from .signals import *
