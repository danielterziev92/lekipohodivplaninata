from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
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
    fields = []
    template_name = None
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        instance = get_object_or_404(Subscribe, slug_to_unsubscribe=slug)
        if instance.is_active:
            instance.is_active = False
            instance.save()
            messages.success(self.request, 'Успешно успяхте да премахнете абонамента си от системата.')
            return redirect(self.success_url)

        messages.error(self.request, 'Не сте абонирани към нашия бюлетин!')
        return redirect(self.success_url)


class MailboxTemplateView(views.TemplateView):
    template_name = 'mailbox.html'
