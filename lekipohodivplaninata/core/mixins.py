import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify

from lekipohodivplaninata.core.utils import from_cyrillic_to_latin, from_str_to_date
from lekipohodivplaninata.hike.models import Hike
from lekipohodivplaninata.users_app.forms import GuideProfileForm
from lekipohodivplaninata.users_app.models import GuideProfile, BaseProfile

HikeModel = Hike


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


class GetHikeForm(object):

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        if self.request.method.lower() == 'post':
            self.generate_slug_field(form)
            self.change_path_of_main_picture(form)

        return form

    @staticmethod
    def generate_slug_field(form):
        slug_prefix = slugify(from_cyrillic_to_latin(form.data["title"]))
        slug_suffix = from_str_to_date(form.data["event_date"])
        form.instance.slug = f'{slug_prefix}-{slug_suffix}'

        return form

    @staticmethod
    def change_path_of_main_picture(form):
        old_path = form.base_fields['main_picture'].options['folder']
        new_path = f'{old_path}/{form.instance.slug}'
        form.base_fields['main_picture'].options['folder'] = new_path

        return form
