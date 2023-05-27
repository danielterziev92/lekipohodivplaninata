import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic as views

from lekipohodivplaninata.base.forms import SignUpHikeForm
from lekipohodivplaninata.core.mixins import HikeUpcomingEvents, HikePassedEvents, UserDataMixin
from lekipohodivplaninata.hike.models import Hike

HikeModel = Hike
UserModel = get_user_model()


class IndexListView(HikeUpcomingEvents, views.ListView):
    template_name = 'index.html'
    paginate_by = 10


class UpcomingEventListView(HikeUpcomingEvents, UserDataMixin, views.ListView):
    template_name = 'hike/upcoming-events.html'
    paginate_by = 10


class PassedEventListView(HikePassedEvents, views.ListView):
    template_name = 'hike/passed-events.html'
    paginate_by = 10


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
