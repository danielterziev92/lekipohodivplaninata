from django.contrib import admin
from django.utils.html import format_html

from lekipohodivplaninata.hike.models import HikeType, HikeMorePicture, HikeLevel, Hike


@admin.register(Hike)
class HikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'thumbnail_image', 'title', 'level', 'duration_time', 'event_date_tag', 'price_tag')
    list_display_links = ('title',)
    prepopulated_fields = {"slug": ("title", "event_date")}
    exclude = ('more_pictures',)

    def main_picture(self, obj):
        return obj.get_main_picture

    def thumbnail_image(self, obj):
        return obj.get_thumbnail_image

    def price_tag(self, obj):
        return obj.get_hike_price

    def event_date_tag(self, obj):
        return obj.get_event_date

    def duration_time(self, obj):
        return obj.get_duration_time

    main_picture.short_description = 'Снимка'
    main_picture.allow_tags = True
    thumbnail_image.short_description = 'Снимка'
    thumbnail_image.allow_tags = True
    price_tag.short_description = 'Цена'
    price_tag.allow_tags = True
    event_date_tag.short_description = 'Дата на събитие'
    event_date_tag.allow_tags = True
    duration_time.short_description = 'Продължителност'


@admin.register(HikeType)
class HikeTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(HikeLevel)
class HikeLevelAdmin(admin.ModelAdmin):
    pass


@admin.register(HikeMorePicture)
class HikeMorePictureAdmin(admin.ModelAdmin):
    pass
