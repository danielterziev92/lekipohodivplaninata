from django.urls import path

from lekipohodivplaninata.hike.views import HikeCreateView, HikeDetailView, HikeListView

urlpatterns = (
    path('create', HikeCreateView.as_view(), name='hike create'),
    path('detail/<int:pk>/<slug:slug>', HikeDetailView.as_view(), name='hike detail'),
    path('list/', HikeListView.as_view(), name='hike list'),
)
