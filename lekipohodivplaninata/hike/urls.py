from django.urls import path, include

from lekipohodivplaninata.hike.views import HikeCreateView, HikeDetailView, HikeListView, HikeUpdateView, \
    HikeDeleteView, HikeMorePictureUpload, HikeTypeCreateView, HikeTypeUpdateView, HikeTypeListView, HikeTypeDeleteView

urlpatterns = (
    path('create/', include([
        path('', HikeCreateView.as_view(), name='hike create'),
        path('type/', HikeTypeCreateView.as_view(), name='hike type create'),
    ])),
    path('update/', include([
        path('type/<int:pk>', HikeTypeUpdateView.as_view(), name='hike type update'),
    ])),
    path('delete/', include([
        path('type/<int:pk>', HikeTypeDeleteView.as_view(), name='hike type delete'),
    ])),
    path('list/', include([
        path('', HikeTypeListView.as_view(), name='hike type list'),
    ])),
    path('<int:pk>/<slug:slug>/', include([
        path('', HikeDetailView.as_view(), name='hike detail'),
        path('update/', HikeUpdateView.as_view(), name='hike update'),
        path('delete/', HikeDeleteView.as_view(), name='hike delete'),
        path('more-pictures/', HikeMorePictureUpload.as_view(), name='hike more pictures'),
    ])),
    path('list/', HikeListView.as_view(), name='hike list'),
)
