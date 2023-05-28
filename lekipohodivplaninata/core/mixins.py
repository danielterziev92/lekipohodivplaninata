import datetime
import random

from cloudinary import api as cloudinary_api, uploader as cloudinary_uploader
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.text import slugify

from lekipohodivplaninata.core.utils import from_cyrillic_to_latin, from_str_to_date
from lekipohodivplaninata.hike.models import Hike
from lekipohodivplaninata.users_app.forms import GuideProfileForm
from lekipohodivplaninata.users_app.models import BaseProfile, GuideProfile

HikeModel = Hike
UserModel = get_user_model()


class UserDataMixin(object):
    @staticmethod
    def generate_random_password(length):
        symbols = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-='
        return ''.join(symbols[random.randint(0, len(symbols) - 1)] for _ in range(length))

    @staticmethod
    def get_user_profile(pk):
        return BaseProfile.objects.get(pk=pk)

    def register_base_user(self, email, first_name, last_name):
        try:
            user = BaseProfile.objects.create(
                user_id=self.register_app_user_with_random_password(email),
                first_name=first_name,
                last_name=last_name
            )
        # IntegrityError - it depends on the database
        except Exception:
            raise ValidationError('Потребител с този имейл адрес вече съществува.')

        return user

    def register_app_user_with_random_password(self, email):
        password = self.generate_random_password(8)
        return UserModel.objects.create(
            email=email,
            password=password,
        )
        # TODO: When implement  async tasks, must send email with password

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=object_list, **kwargs)

        if isinstance(self.request.user, UserModel):
            context_data['user'] = self.get_user_profile(self.request.user.pk)

        return context_data


class UserFormMixin(object):

    def get_model(self):
        model = BaseProfile

        if self.request.user.is_staff:
            model = GuideProfile

        return model

    def get_form_clas_form(self):
        if self.request.user.is_staff:
            return GuideProfileForm

        return None

    def get_fields_form(self, *args):
        fields = None
        if not self.request.user.is_staff:
            fields = tuple(args)
            return fields

        return fields

    def get_object(self, queryset=None):
        model = self.model

        if self.request.user.is_staff:
            try:
                obj = model.objects.get(pk=self.request.user.pk)
            except ObjectDoesNotExist:
                obj = model.objects.create(
                    user_id_id=self.request.user.pk,
                    profile_id_id=self.request.user.pk,
                    date_of_birth=datetime.datetime.today(),
                    description='Тук трябва да въведете описание.',
                    certificate='image/upload/v1683563916/user-avatar_cyynjj.png',
                    avatar='image/upload/v1683563916/user-avatar_cyynjj.png',
                )
        else:
            obj = model.objects.get(pk=self.request.user.pk)

        return obj


class PicturesMixin:
    @staticmethod
    def upload_picture(file, folder):
        data = cloudinary_uploader.upload(file=file, folder=folder)
        return f'{data["public_id"]}.{data["format"]}'

    @staticmethod
    def delete_pictures(files: list):
        cloudinary_api.delete_resources(files)

    @staticmethod
    def delete_folder(folder: str):
        cloudinary_api.delete_folder(folder)

    @staticmethod
    def get_picture_folder(public_id: str):
        return '/'.join(public_id.split('/')[:2])

    @staticmethod
    def create_folder(folder_name):
        return cloudinary_api.create_folder(folder_name)

    @staticmethod
    def move_picture_to_new_folder(old_public_id, new_public_id):
        return cloudinary_uploader.rename(old_public_id, new_public_id)


class HikeBaseFormMixin(PicturesMixin, object):
    def transfer_picture_to_new_folder(self, obj):
        img_name = self.get_img_name_from_public_id(obj.main_picture)
        old_folder = self.get_picture_folder(obj.main_picture.public_id)
        new_folder = self.create_folder(self.get_picture_folder(obj.slug))
        old_public_id = obj.main_picture.public_id
        new_public_id = f'{self.generate_folder_name(new_folder["path"])}/{img_name}'
        obj.main_picture.public_id = self.move_picture_to_new_folder(old_public_id, new_public_id)['public_id']
        self.delete_folder(old_folder)

    @staticmethod
    def generate_slug_field(title: str, event_date):
        slug_prefix = slugify(from_cyrillic_to_latin(title))
        slug_suffix = from_str_to_date(event_date)
        slug = f'{slug_prefix}-{slug_suffix}'

        return slug

    @staticmethod
    def get_img_name_from_public_id(img):
        return img.public_id.split('/').pop()

    @staticmethod
    def generate_folder_name(slug: str):
        return f'{HikeModel.PICTURE_DIRECTORY}/{slug}'


class HikeCreateFormMixin(HikeBaseFormMixin):
    def save(self, commit=True):
        obj = super().save(commit=False)
        obj = self.create_obj(obj)
        if commit:
            obj.save()

        return obj

    def create_obj(self, obj):
        obj.slug = self.generate_slug_field(obj.title, obj.event_date)
        folder = self.generate_folder_name(obj.slug)
        obj.main_picture = self.upload_picture(self.cleaned_data['main_picture'].file, folder)
        return obj


class HikeUpdateFormMixin(HikeBaseFormMixin):
    def save(self, commit=True):
        obj = super().save(commit=False)
        obj = self.edit_obj(obj)
        if commit:
            obj.save()

        return obj

    def edit_obj(self, obj):
        db_obj = HikeModel.objects.get(pk=obj.pk)

        if self.cleaned_data['title'] != db_obj.title or self.cleaned_data['event_date'] != db_obj.event_date:
            obj.slug = self.generate_slug_field(obj.title, obj.event_date)
            self.transfer_picture_to_new_folder(obj)

        if self.cleaned_data['new_main_picture']:
            try:
                folder = self.get_picture_folder(obj.main_picture.public_id)
            except Exception:
                folder_name = self.generate_folder_name(obj.slug)
                folder = self.get_picture_folder(folder_name)

            if obj.main_picture.public_id is not None:
                self.delete_pictures([obj.main_picture.public_id])
            # AttributeError("'InMemoryUploadedFile' object has no attribute 'file'")
            try:
                obj.main_picture = self.upload_picture(self.cleaned_data['new_main_picture'].file, folder)
            except InMemoryUploadedFile:
                raise ValidationError('Моля изберете файл')

        return obj


class HikeUpcomingEvents(object):
    def get_queryset(self):
        return HikeModel.objects.all().filter(event_date__gt=datetime.date.today()).order_by('event_date')


class HikePassedEvents(object):
    def get_queryset(self):
        return HikeModel.objects.all().filter(event_date__lt=datetime.date.today()).order_by('-event_date')
