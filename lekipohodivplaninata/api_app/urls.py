from django.urls import path, re_path, include

from lekipohodivplaninata.api_app.views import SubscribeListAndCreateAPIView, HikeSearchAPIView, AdminEmailListAPIView, \
    IMAPSettingsCreateAPIView, IMAPSettingsAPIView

urlpatterns = (
    path('subscribers/', SubscribeListAndCreateAPIView.as_view(), name='subscribers-list-create'),
    re_path(r'hikes/search/$', HikeSearchAPIView.as_view(), name='hike-search'),
    path('mailbox/', AdminEmailListAPIView.as_view(), name='mailbox'),
    path('imap-settings/', IMAPSettingsCreateAPIView.as_view(), name='imap-settings-create'),
    path('imap-settings/<int:pk>/', IMAPSettingsAPIView.as_view(), name='imap-settings'),
)
