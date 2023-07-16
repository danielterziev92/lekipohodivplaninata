from django.urls import path, include

from lekipohodivplaninata.hike.views.hike import HikeCreateView, HikeDetailView, HikeUpdateView, HikeDeleteView, \
    HikeListView
from lekipohodivplaninata.hike.views.hike_level import HikeLevelCreateView, HikeLevelUpdateView, HikeLevelListView, \
    HikeLevelDeleteView
from lekipohodivplaninata.hike.views.hike_more_picture import HikeMorePictureCreate, HikeMorePictureDeleteView, \
    HikeMorePictureListView
from lekipohodivplaninata.hike.views.hike_types import HikeTypeCreateView, HikeTypeUpdateView, HikeTypeListView, \
    HikeTypeDeleteView

urlpatterns = (
    path('create/', include([
        path('', HikeCreateView.as_view(), name='hike create'),
        path('type/', HikeTypeCreateView.as_view(), name='hike type create'),
        path('level/', HikeLevelCreateView.as_view(), name='hike level create'),
    ])),
    path('update/', include([
        path('type/<int:pk>/', HikeTypeUpdateView.as_view(), name='hike type update'),
        path('level/<int:pk>/', HikeLevelUpdateView.as_view(), name='hike level update'),
    ])),
    path('delete/', include([
        path('type/<int:pk>/', HikeTypeDeleteView.as_view(), name='hike type delete'),
        path('level/<int:pk>/', HikeLevelDeleteView.as_view(), name='hike level delete'),
    ])),
    path('list/', include([
        path('', HikeListView.as_view(), name='hike list'),
        path('types/', HikeTypeListView.as_view(), name='hike type list'),
        path('level/', HikeLevelListView.as_view(), name='hike level list'),
    ])),
    path('<int:pk>/<slug:slug>/', include([
        path('', HikeDetailView.as_view(), name='hike detail'),
        path('update/', HikeUpdateView.as_view(), name='hike update'),
        path('delete/', HikeDeleteView.as_view(), name='hike delete'),
    ])),
    path('more-pictures/<slug:slug>/', include([
        path('add/', HikeMorePictureCreate.as_view(), name='hike more pictures add'),
        path('delete/<int:pk>', HikeMorePictureDeleteView.as_view(), name='hike more pictures delete'),
        path('list/', HikeMorePictureListView.as_view(), name='hike more pictures list'),
    ])),
)
