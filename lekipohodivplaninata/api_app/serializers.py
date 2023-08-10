from rest_framework import serializers

from lekipohodivplaninata.api_app.models import Subscribe


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'
