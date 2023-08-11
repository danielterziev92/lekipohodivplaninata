from rest_framework import serializers

from lekipohodivplaninata.api_app.models import Subscribe
from lekipohodivplaninata.core.mixins import CommonMixin


class SubscribeSerializer(CommonMixin, serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ('email',)

    def create(self, validated_data):
        slug = self.generate_random_string(16)
        subscribe = Subscribe.objects.create(
            email=validated_data['email'],
            slug_to_unsubscribe=slug
        )

        return subscribe
