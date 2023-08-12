from rest_framework import generics as rest_views, status
from rest_framework.response import Response

from lekipohodivplaninata.api_app.models import Subscribe
from lekipohodivplaninata.api_app.serializers import SubscribeSerializer


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
