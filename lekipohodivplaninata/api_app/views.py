from rest_framework import generics as rest_views

from lekipohodivplaninata.api_app.models import Subscribe
from lekipohodivplaninata.api_app.serializers import SubscribeSerializer


class SubscribeListAndCreateAPIView(rest_views.ListCreateAPIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
