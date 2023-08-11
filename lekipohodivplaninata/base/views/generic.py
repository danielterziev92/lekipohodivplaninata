from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views

from lekipohodivplaninata.api_app.models import Subscribe
from lekipohodivplaninata.base.models import Slider
from lekipohodivplaninata.core.mixins import HikeUpcomingEvents, HikePassedEvents, UserDataMixin
from lekipohodivplaninata.hike.models import Hike

HikeModel = Hike


class IndexListView(HikeUpcomingEvents, views.ListView):
    template_name = 'index.html'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['sliders'] = Slider.objects.all()

        return context_data


class UpcomingEventListView(HikeUpcomingEvents, UserDataMixin, views.ListView):
    template_name = 'hike/upcoming-events.html'
    paginate_by = 10


class PassedEventListView(HikePassedEvents, views.ListView):
    template_name = 'hike/passed-events.html'
    paginate_by = 10


class UnsubscribeView(views.UpdateView):
    model = Subscribe
    fields = ('is_active',)
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Subscribe, slug_to_unsubscribe=slug)

    def form_valid(self, form):
        form.instance.is_active = False
        messages.success(self.request, 'Успешно успяхте да премахнете абонамента си от системата.')
        return super().form_valid(form)
