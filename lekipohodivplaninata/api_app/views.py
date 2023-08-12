import email
import imaplib
import smtplib
from email.message import EmailMessage

from rest_framework import generics as rest_views, status, views as api_views
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db import models

from lekipohodivplaninata.api_app.models import Subscribe, IMAPSettings
from lekipohodivplaninata.api_app.serializers import SubscribeSerializer, HikeSerializer, IMAPSettingsSerializer
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
            ).order_by('-event_date')
        return hikes

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        return Response({
            'hike': serializer.data,
        }, status=status.HTTP_200_OK)


@permission_classes([IsAdminUser, IsAuthenticated])
class AdminEmailListAPIView(api_views.APIView):
    def get(self, request, *args, **kwargs):
        try:
            imap_settings = IMAPSettings.objects.first()

            if not imap_settings:
                return Response({
                    'error': 'Настройките за IMAP услугата не са конфигурирани'
                }, status=status.HTTP_400_BAD_REQUEST)

            mailbox = imaplib.IMAP4_SSL(imap_settings.imap_server, imap_settings.imap_port)
            mailbox.login(imap_settings.imap_username, imap_settings.imap_password)
            mailbox.select('INBOX')

            _, data = mailbox.search(None, 'ALL')
            message_ids = data[0].split()

            email_list = []

            for message_id in message_ids:
                _, msg_data = mailbox.fetch(message_id, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])

                subject = msg['subject']
                sender = msg['from']

                if msg.is_multipart():
                    body = ''
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload(decode=True).decode('utf-8')
                            break
                else:
                    body = msg.get_payload(decode=True).decode('utf-8')

                email_list.append({
                    'subject': subject,
                    'sender': sender,
                    'body': body
                })

            mailbox.logout()
            return Response(email_list, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': 'Грешка при получаването на имейли',
                'exception': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            recipient = request.data.get('recipient')
            subject = request.data.get('subject')
            body = request.data.get('body')

            imap_settings = IMAPSettings.objects.first()
            if not imap_settings:
                return Response({
                    'error': 'Настройките за IMAP услугата не са конфигурирани'
                }, status=status.HTTP_400_BAD_REQUEST)

            msg = EmailMessage()
            msg.set_content("This is the email body.")
            msg["Subject"] = subject
            msg["From"] = recipient
            msg["To"] = recipient

            smtp_server = smtplib.SMTP(imap_settings.imap_server, imap_settings.imap_port)
            smtp_server.starttls()
            smtp_server.login(imap_settings.imap_username, imap_settings.imap_password)

            smtp_server.send_message(msg)
            smtp_server.quit()

            return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': 'Грешка при изпращането на имейл',
                'exception': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IMAPSettingsCreateAPIView(rest_views.CreateAPIView):
    queryset = IMAPSettings.objects.all()
    serializer_class = IMAPSettingsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class IMAPSettingsAPIView(rest_views.RetrieveUpdateDestroyAPIView):
    queryset = IMAPSettings.objects.all()
    serializer_class = IMAPSettingsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
