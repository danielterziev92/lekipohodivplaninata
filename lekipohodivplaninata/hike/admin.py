from django.contrib import admin

from lekipohodivplaninata.hike.models import HikeType, HikeMorePicture, HikeLevel, Hike


@admin.register(Hike)
class HikeAdmin(admin.ModelAdmin):
    pass


@admin.register(HikeType)
class HikeTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(HikeLevel)
class HikeLevelAdmin(admin.ModelAdmin):
    pass


@admin.register(HikeMorePicture)
class HikeMorePictureAdmin(admin.ModelAdmin):
    pass
