from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import handler400, handler403, handler404, handler500
from django.urls import path, include

from lekipohodivplaninata.base.error_views import bad_request_view, permission_denied_view, page_not_fount_view, \
    server_error_view

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('users/', include('lekipohodivplaninata.users_app.urls')),
                  path('hike/', include('lekipohodivplaninata.hike.urls')),
                  path('', include('lekipohodivplaninata.base.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = bad_request_view
handler404 = page_not_fount_view
