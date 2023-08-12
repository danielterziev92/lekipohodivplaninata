from rest_framework import generics as rest_views, status
from rest_framework.response import Response
from django.db import models

from lekipohodivplaninata.api_app.models import Subscribe
from lekipohodivplaninata.api_app.serializers import SubscribeSerializer, HikeSerializer
from lekipohodivplaninata.hike.models import Hike


class SubscribeListAndCreateAPIView(rest_views.ListCreateAPIView):
    queryset = Subscribe.objects.all().order_by('-subscribed_at')
    serializer_class = SubscribeSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        query = Subscribe.objects.filter(email=email).first()
        if query:
            if query.is_active == False:
                query.is_active = True
                query.save()
                return super().post(request, *args, **kwargs)

            return Response({
                'message': 'Имейлът вече е записан за бюлетина ни.'
            }, status=status.HTTP_409_CONFLICT)

        return super().post(request, *args, **kwargs)


class HikeSearchAPIView(rest_views.ListCreateAPIView):
    serializer_class = HikeSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('q', '')
        hikes = []

        if search_query:
            hikes = Hike.objects.filter(
                models.Q(title__icontains=search_query) |
                models.Q(description__icontains=search_query)
            ).order_by('event_date')
        return hikes

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        return Response({
            'hike': serializer.data,
        }, status=status.HTTP_200_OK)
