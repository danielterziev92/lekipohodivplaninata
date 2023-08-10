from django.db import modelsrouter = DefaultRouter()
router.register(r'subscribe', )


class Subscribe(models.Model):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    slug_to_unsubscribe = models.SlugField(
        unique=True,
        null=False,
        blank=True,
    )

    subscribed_at = models.DateTimeField(
        auto_now_add=True,
    )
