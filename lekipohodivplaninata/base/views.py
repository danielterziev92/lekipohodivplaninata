from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from lekipohodivplaninata.base.forms import SignUpHikeForm, SiteEvaluationForm
from lekipohodivplaninata.base.forms import SignedForHikeUpdateForm
from lekipohodivplaninata.base.models import SignUpForHike
from lekipohodivplaninata.core.mixins import HikeUpcomingEvents, HikePassedEvents, UserDataMixin
from lekipohodivplaninata.hike.models import Hike
from lekipohodivplaninata.users_app.models import BaseProfile

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
    template_name = ''
    form_class = SignUpHikeForm
    success_url = reverse_lazy('site evaluation')

    def get_success_url(self):
        cache.set('is_signed', True, timeout=60)
        return reverse_lazy('site evaluation')

    def get_queryset(self):
        return Hike.objects.all()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class SignedForHikeUpdateView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.UpdateView):
    template_name = 'hike/signed-for-hike.html'
    permission_required = 'is_staff'
    form_class = SignedForHikeUpdateForm
    model = SignUpForHike

    def get_success_url(self):
        obj = SignUpForHike.objects.get(pk=self.kwargs.get('pk'))
        return reverse_lazy('all signed for hike', kwargs={
            'pk': obj.hike_id.pk, 'slug': obj.hike_id.slug,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_info = BaseProfile.objects.get(pk=context['object'].user_id)
        context['form'].fields['first_name'].widget.attrs['value'] = user_info.get_first_name
        context['form'].fields['last_name'].widget.attrs['value'] = user_info.get_last_name
        context['form'].fields['phone_number'].widget.attrs['value'] = user_info.phone_number
        return context


class SignedForHikeListView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.ListView):
    template_name = 'hike/all-signed-for-hike.html'
    permission_required = 'is_staff'

    def get_queryset(self):
        return SignUpForHike.objects.filter(hike_id=self.kwargs['pk']).order_by('travel_with')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title_of_hike'] = get_object_or_404(Hike, pk=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))
        return context


class SiteEvaluationView(views.CreateView):
    template_name = 'site-evaluation.html'
    form_class = SiteEvaluationForm
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if cache.get('is_signed'):
            cache.delete('is_signed')
            return super().get(request, *args, **kwargs)

        return redirect('index')
