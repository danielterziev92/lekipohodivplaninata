from django.urls import path

from lekipohodivplaninata.api_app.views import SubscribeListAndCreateAPIView

urlpatterns = (
    path('subscribers/', SubscribeListAndCreateAPIView.as_view(), name='subscribers-list-create'),
)
