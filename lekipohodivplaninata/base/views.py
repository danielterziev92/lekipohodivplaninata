from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins, get_user_model
from django.utils.translation import gettext_lazy as _

from lekipohodivplaninata.base.forms import SignUpHikeForm, SiteEvaluationForm, SignedForHikeUpdateForm, \
    SliderCreateForm, SliderEditForm
from lekipohodivplaninata.base.models import SignUpForHike, Slider
from lekipohodivplaninata.core.mixins import HikeUpcomingEvents, HikePassedEvents, UserDataMixin
from lekipohodivplaninata.core.mixins import PicturesMixin
from lekipohodivplaninata.hike.models import Hike
from lekipohodivplaninata.users_app.models import BaseProfile

HikeModel = Hike
UserModel = get_user_model()


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


class SignUpHike(views.UpdateView):
    template_name = 'hike/sign-for-hike.html'
    model = Hike
    form_class = SignUpHikeForm

    def get_success_url(self):
        cache.set('is_signed', True, timeout=60)
        return reverse_lazy('site evaluation')

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


def confirm_user_for_hike(request, pk, text):
    bool_values = {
        'True': True,
        'False': False,
    }

    if request.method.lower() == 'post':
        return redirect('index')

    obj = get_object_or_404(SignUpForHike, pk=pk)
    if bool_values[text]:
        obj.is_confirmed = True
        obj.save()
    else:
        obj.delete()

    return redirect('all signed for hike', pk=obj.hike_id.pk, slug=obj.hike_id.slug)


# TODO: Refactor this for recommend
def recommend_user_for_hike(request, pk):
    if request.method.lower() == 'post':
        return redirect('index')

    obj = get_object_or_404(SignUpForHike, pk=pk)
    obj.is_confirmed = False
    obj.save()

    return redirect('all signed for hike', pk=obj.hike_id.pk, slug=obj.hike_id.slug)


class SignedForHikeListView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.ListView):
    template_name = 'hike/all-signed-for-hike.html'
    permission_required = 'is_staff'

    def get_queryset(self):
        return SignUpForHike.objects.filter(hike_id=self.kwargs['pk']) \
            .order_by('is_confirmed').order_by('is_recommend').order_by('travel_with')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['hike'] = get_object_or_404(Hike, pk=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))
        return context


class SiteEvaluationView(views.CreateView):
    template_name = 'evaluation.html'
    form_class = SiteEvaluationForm
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Моля да оцените сайта ни:',
        'action_url': _('site evaluation')
    }

    def get(self, request, *args, **kwargs):
        if cache.get('is_signed'):
            cache.delete('is_signed')
            return super().get(request, *args, **kwargs)

        return redirect('index')


class SliderCreateView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.CreateView):
    permission_required = 'is_staff'
    template_name = 'slider/create.html'
    form_class = SliderCreateForm
    success_url = reverse_lazy('slider list')


class SliderListView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.ListView):
    permission_required = 'is_staff'
    template_name = 'slider/list.html'
    model = Slider

    def get_queryset(self):
        return Slider.objects.all().order_by('hike_id__event_date')


class SliderEditView \
            (PicturesMixin, auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.UpdateView):
    permission_required = 'is_staff'
    template_name = 'slider/edit.html'
    form_class = SliderEditForm
    model = Slider
    success_url = reverse_lazy('slider list')


class SliderDeleteView \
            (PicturesMixin, auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.DeleteView):
    permission_required = 'is_staff'
    template_name = 'slider/delete.html'
    model = Slider
    success_url = reverse_lazy('slider list')

    def form_valid(self, form):
        public_id = self.object.image.public_id
        self.delete_pictures(public_id)
        folder = self.get_picture_folder(public_id=public_id)
        self.delete_folder(folder=folder)

        return super().form_valid(form=form)
