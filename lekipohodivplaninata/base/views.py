from django.contrib.auth import get_user_model
from django.views import generic as views

from lekipohodivplaninata.base.forms import SignUpHikeForm
from lekipohodivplaninata.base.models import SignUpForHike
from lekipohodivplaninata.hike.models import Hike
from lekipohodivplaninata.users_app.models import BaseProfile

HikeModel = Hike
UserModel = get_user_model()


class IndexPageTemplateView(views.ListView):
    template_name = 'index.html'
    paginate_by = 10

    def get_queryset(self):
        return HikeModel.objects.all().order_by('event_date')


# def sign_up_for_hike(request):
#     if request.method.lower() == 'get':
#         pass


class SignUpHike(views.UpdateView):
    template_name = 'hike/sign-up-for-hike.html'
    model = SignUpForHike
    form_class = SignUpHikeForm

    def get(self, request, *args, **kwargs):
        if isinstance(self.request.user, UserModel):
            user = self.get_user_profile(self.request.user.pk)

        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        # kwargs['from_url'] = self.request.META.get('HTTP_REFERER')
        return kwargs

    @staticmethod
    def get_user_profile(user_id):
        return BaseProfile.objects.get(pk=user_id)
