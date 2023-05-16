from django.urls import path, include

from lekipohodivplaninata.hike.views import HikeCreateView, HikeDetailView, HikeListView, HikeUpdateView

urlpatterns = (
    path('create', HikeCreateView.as_view(), name='hike create'),
    path('<int:pk>/<slug:slug>', include([
        path('', HikeDetailView.as_view(), name='hike detail'),
        path('/update', HikeUpdateView.as_view(), name='hike update'),
        path('/delete', HikeUpdateView.as_view(), name='hike delete'),
    ])),
    path('list/', HikeListView.as_view(), name='hike list'),
)
