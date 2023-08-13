from django.contrib import admin
from django.db import transaction
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from lekipohodivplaninata.core.mixins import PicturesMixin
from lekipohodivplaninata.core.utils import from_cyrillic_to_latin, from_str_to_date
from lekipohodivplaninata.hike.models import HikeType, HikeMorePicture, HikeLevel, Hike


@admin.register(Hike)
class HikeAdmin(admin.ModelAdmin, PicturesMixin):
    list_display = ('id', 'thumbnail_image', 'title', 'level', 'duration_time', 'event_date_tag', 'price_tag')
    list_display_links = ('title',)
    prepopulated_fields = {"slug": ("title", "event_date")}
    readonly_fields = ('display_images_preview',)
    exclude = ('more_pictures',)
    actions = ('delete_object_with_pictures',)

    def main_picture(self, obj):
        return obj.get_main_picture

    def thumbnail_image(self, obj):
        return obj.get_thumbnail_image

    def display_images_preview(self, obj):
        return self.thumbnail_image(obj)

    def price_tag(self, obj):
        return obj.get_hike_price

    def event_date_tag(self, obj):
        return obj.get_event_date

    def duration_time(self, obj):
        return obj.get_duration_time

    def save_model(self, request, obj, form, change):
        if not change:
            try:
                with transaction.atomic():
                    obj = self.create_obj(obj)
                    obj.save()
            except Exception as e:
                public_id, _ = obj.main_picture.split('.')
                folder = '/'.join(public_id.split('/')[:2])
                self.destroy_picture_by_url(public_id)
                self.delete_folder(folder)
                transaction.rollback()

        if change:
            obj.slug = self.generate_slug_field(obj.title, obj.event_date)
            self.transfer_picture_to_new_folder(obj)

        super().save_model(request, obj, form, change)

    def transfer_picture_to_new_folder(self, obj):
        img_name = self.get_img_name_from_public_id(obj.main_picture)
        old_folder = self.get_picture_folder(obj.main_picture.public_id)
        new_folder = self.create_folder(self.get_picture_folder(obj.slug))
        old_public_id = obj.main_picture.public_id
        new_public_id = f'{self.generate_folder_name(new_folder["path"])}/{img_name}'
        obj.main_picture.public_id = self.move_picture_to_new_folder(old_public_id, new_public_id)['public_id']
        self.delete_folder(old_folder)

    @staticmethod
    def get_img_name_from_public_id(img):
        return img.public_id.split('/').pop()

    @staticmethod
    def generate_folder_name(slug: str):
        return f'{Hike.PICTURE_DIRECTORY}/{slug}'

    @staticmethod
    def generate_slug_field(title: str, event_date):
        slug_prefix = slugify(from_cyrillic_to_latin(title))
        slug_suffix = from_str_to_date(event_date)
        slug = f'{slug_prefix}-{slug_suffix}'

        return slug

    def create_obj(self, obj):
        obj.slug = self.generate_slug_field(obj.title, obj.event_date)
        folder = self.generate_folder_name(obj.slug)
        obj.main_picture = self.upload_picture(obj.main_picture.file, folder)

        return obj

    def delete_object_with_pictures(self, request, queryset):
        for obj in queryset:
            self.delete_hike_pictures(obj)
            obj.delete()

        self.message_user(
            request,
            f'Успешно изтрихте {queryset.count()} {"похода" if queryset.count() > 1 else "поход"}.'
        )

    def delete_hike_pictures(self, model):
        pictures_public_ids = []
        if isinstance(model, HikeMorePicture):
            return

        if isinstance(model, Hike):
            more_pictures = model.more_pictures.all()

            if more_pictures:
                for picture in more_pictures:
                    pictures_public_ids.append(picture.image.public_id)

            main_picture_public_id = model.main_picture.public_id
            pictures_public_ids.append(main_picture_public_id)
            self.delete_pictures(pictures_public_ids)

            main_picture_folder = self.get_picture_folder(main_picture_public_id)
            self.delete_pictures(main_picture_folder)

            return

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    main_picture.short_description = 'Снимка'
    main_picture.allow_tags = True
    thumbnail_image.short_description = 'Снимка'
    thumbnail_image.allow_tags = True
    price_tag.short_description = 'Цена'
    price_tag.allow_tags = True
    event_date_tag.short_description = 'Дата на събитие'
    event_date_tag.allow_tags = True
    duration_time.short_description = 'Продължителност'
    display_images_preview.short_description = 'Преглед на основната снимка'
    delete_object_with_pictures.short_description = 'Изтриване на всички снимки и похода'


@admin.register(HikeType)
class HikeTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(HikeLevel)
class HikeLevelAdmin(admin.ModelAdmin):
    pass
