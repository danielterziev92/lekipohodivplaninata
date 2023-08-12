from django.db import models


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


class IMAPSettings(models.Model):
    IMAP_SERVER_MAX_LENGTH = 100
    IMAP_USERNAME_MAX_LENGTH = 100
    IMAP_PASSWORD_MAX_LENGTH = 100

    imap_server = models.CharField(
        max_length=IMAP_SERVER_MAX_LENGTH,
        null=False,
        blank=False,
    )

    imap_port = models.PositiveSmallIntegerField()

    imap_username = models.CharField(
        max_length=IMAP_USERNAME_MAX_LENGTH,
        null=False,
        blank=False,
    )

    imap_password = models.CharField(
        max_length=IMAP_PASSWORD_MAX_LENGTH,
        null=False,
        blank=False,
    )
