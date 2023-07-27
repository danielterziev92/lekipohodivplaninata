from django.urls import path, include

from lekipohodivplaninata.base.views.evaluations import SiteEvaluationView, SiteEvaluationListView
from lekipohodivplaninata.base.views.generic import IndexListView, UpcomingEventListView, PassedEventListView
from lekipohodivplaninata.base.views.sign_up_for_hike import SignedForHikeUpdateView, confirm_user_for_hike, \
    presence_user_for_hike, SignUpHike, SignedForHikeListView
from lekipohodivplaninata.base.views.slider import SliderCreateView, SliderEditView, SliderDeleteView, SliderListView

urlpatterns = (
    path('', IndexListView.as_view(), name='index'),
    path('upcoming/', UpcomingEventListView.as_view(), name='hikes-upcoming'),
    path('passed/', PassedEventListView.as_view(), name='hikes-passed'),
    path('recorded/<int:pk>/edit/', SignedForHikeUpdateView.as_view(), name='signed-for-hike-update'),
    path('recorded/<int:pk>/confirmed/<str:text>', confirm_user_for_hike, name='signed-for-hike-confirming'),
    path('is_presence/<int:pk>/confirmed/<str:text>', presence_user_for_hike, name='signed-for-hike-presence'),
    path('<int:pk>/<slug:slug>/', include([
        path('sign-up/', SignUpHike.as_view(), name='sign-up-for-hike'),
        path('all-recorded/', SignedForHikeListView.as_view(), name='all-signed-for-hike')
    ])),
    path('site-evaluation/', include([
        path('', SiteEvaluationView.as_view(), name='site-evaluation'),
        path('all/', SiteEvaluationListView.as_view(), name='site-evaluation-all')
    ])),
    path('slider/', include([
        path('', SliderListView.as_view(), name='slider-list'),
        path('create/', SliderCreateView.as_view(), name='slider-create'),
        path('edit/<int:pk>', SliderEditView.as_view(), name='slider-edit'),
        path('delete/<int:pk>', SliderDeleteView.as_view(), name='slider-delete'),
    ]))
)
