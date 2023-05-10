import datetime

from django.core.exceptions import ObjectDoesNotExist

from lekipohodivplaninata.users_app.forms import GuideProfileForm
from lekipohodivplaninata.users_app.models import GuideProfile, BaseProfile


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
