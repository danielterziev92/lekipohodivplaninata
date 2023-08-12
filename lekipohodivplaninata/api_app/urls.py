from django.urls import path, re_path

from lekipohodivplaninata.api_app.views import SubscribeListAndCreateAPIView, HikeSearchAPIView

urlpatterns = (
    path('subscribers/', SubscribeListAndCreateAPIView.as_view(), name='subscribers-list-create'),
    re_path(r'hikes/search/$', HikeSearchAPIView.as_view(), name='hike-search'),
)
