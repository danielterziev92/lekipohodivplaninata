from django.urls import path, include

from lekipohodivplaninata.hike.views import HikeCreateView, HikeDetailView, HikeListView, HikeUpdateView, \
    HikeDeleteView, HikeMorePictureUpload

urlpatterns = (
    path('create', HikeCreateView.as_view(), name='hike create'),
    path('<int:pk>/<slug:slug>/', include([
        path('', HikeDetailView.as_view(), name='hike detail'),
        path('update', HikeUpdateView.as_view(), name='hike update'),
        path('delete', HikeDeleteView.as_view(), name='hike delete'),
        path('more-pictures', HikeMorePictureUpload.as_view(), name='hike more pictures'),
    ])),
    path('list', HikeListView.as_view(), name='hike list'),
)
