from rest_framework import generics as rest_views

from lekipohodivplaninata.api_app.models import Subscribe
from lekipohodivplaninata.api_app.serializers import SubscribeSerializer


class SubscribeListAndCreateAPIView(rest_views.ListCreateAPIView):
    queryset = Subscribe.objects.all().order_by('-subscribed_at')
    serializer_class = SubscribeSerializer
