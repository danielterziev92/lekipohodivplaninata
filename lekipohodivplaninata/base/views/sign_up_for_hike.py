from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from lekipohodivplaninata.base.forms import SignUpHikeForm, SignedForHikeUpdateForm
from lekipohodivplaninata.base.models import SignUpForHike, Hike
from lekipohodivplaninata.users_app.models import BaseProfile

from lekipohodivplaninata.core.mixins import UserDataMixin


class SignUpHike(views.UpdateView):
    template_name = 'hike/sign-for-hike.html'
    model = Hike
    form_class = SignUpHikeForm

    def get_success_url(self):
        cache.set('is_signed', True, timeout=60)
        return reverse_lazy('site-evaluation')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Вие успешно се записахте за похода.')
        return super().form_valid(form)


class SignedForHikeUpdateView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.UpdateView):
    template_name = 'hike/signed-for-hike.html'
    permission_required = 'is_staff'
    form_class = SignedForHikeUpdateForm
    model = SignUpForHike

    def get_success_url(self):
        obj = SignUpForHike.objects.get(pk=self.kwargs.get('pk'))
        return reverse_lazy('all-signed-for-hike', kwargs={
            'pk': obj.hike_id.pk, 'slug': obj.hike_id.slug,
        })

    def form_valid(self, form):
        cache.set('signed_for_hike_edit_info', True)
        return super().form_valid(form)

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

    Model = UserDataMixin.get_current_user_model(obj.user_type)
    user = Model.objects.filter(pk=obj.user_id).get()

    if bool_values[text]:
        obj.is_confirmed = True
        messages.success(request, f'Успешно потвърдихте {user.get_full_name} за поход {obj.hike_id.title}.')
        obj.save()
    else:
        messages.success(request, f'Успешно премахнахте {user.get_full_name} за поход {obj.hike_id.title}.')
        obj.delete()

    return redirect('all-signed-for-hike', pk=obj.hike_id.pk, slug=obj.hike_id.slug)


def presence_user_for_hike(request, pk, text):
    bool_values = {
        'True': True,
        'False': False,
    }
    if request.method.lower() == 'post':
        return redirect('index')

    obj = get_object_or_404(SignUpForHike, pk=pk)
    obj.is_presence = bool_values[text]

    Model = UserDataMixin.get_current_user_model(obj.user_type)
    user = Model.objects.filter(pk=obj.user_id).get()

    messages.success(request, f'Успешно отбелязохте {user.get_full_name}!')

    obj.save()

    return redirect('all-signed-for-hike', pk=obj.hike_id.pk, slug=obj.hike_id.slug)


class SignedForHikeListView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.ListView):
    template_name = 'hike/all-signed-for-hike.html'
    permission_required = 'is_staff'

    def get_queryset(self):
        return SignUpForHike.objects.filter(hike_id=self.kwargs['pk']) \
            .order_by('is_confirmed').order_by('is_presence').order_by('travel_with')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['hike'] = get_object_or_404(Hike, pk=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))
        return context
