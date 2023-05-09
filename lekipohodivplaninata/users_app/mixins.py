from lekipohodivplaninata.users_app.forms import GuideProfileForm
from lekipohodivplaninata.users_app.models import GuideProfile, BaseProfile


class UserFormMixin(object):

    def get_model_form(self):
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


