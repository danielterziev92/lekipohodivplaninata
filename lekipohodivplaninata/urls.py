from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('users/', include('lekipohodivplaninata.users_app.urls')),
                  path('hike/', include('lekipohodivplaninata.hike.urls')),
                  path('', include('lekipohodivplaninata.base.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
