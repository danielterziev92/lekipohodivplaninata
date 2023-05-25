from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy
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


class SignUpHike(views.UpdateView):
    template_name = 'hike/sign-up-for-hike.html'
    # model = SignUpForHike
    form_class = SignUpHikeForm
    success_url = reverse_lazy('index')

    def get_queryset(self):
        return Hike.objects.all()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ASDS(views.CreateView):
    template_name = 'hike/sign-up-for-hike2.html'

