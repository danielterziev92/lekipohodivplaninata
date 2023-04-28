from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('lekipohodivplaninata.base.urls')),
                  path('users/', include('lekipohodivplaninata.users_app.urls')),
                  path('hike', include('lekipohodivplaninata.hike.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# SITE_NAME = "lekipohodivplaninata.BG"
# admin.site.site_header = f"{SITE_NAME} Админ Панел"
# admin.site.site_title = f"{SITE_NAME} Admin Portal"
# admin.site.index_title = f"Welcome to {SITE_NAME} Admin Portal"
