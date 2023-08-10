from django.contrib import messages
from django.db.models import RestrictedError
from django.http import HttpResponseRedirect
from django.views import generic as views
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth import mixins as auth_mixins

from lekipohodivplaninata.hike.forms import HikeLevelForm
from lekipohodivplaninata.hike.models import HikeLevel


class HikeLevelCreateView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.CreateView):
    template_name = 'hike/templates/create-or-update.html'
    permission_required = 'is_staff'
    form_class = HikeLevelForm
    success_url = reverse_lazy('hike-level-list')

    def form_valid(self, form):
        messages.success(self.request, f'Успешно създадохте ниво за поход.')
        return super().form_valid(form)


class HikeLevelUpdateView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.UpdateView):
    template_name = 'hike/templates/create-or-update.html'
    permission_required = 'is_staff'
    form_class = HikeLevelForm
    model = HikeLevel
    success_url = reverse_lazy('hike-level-list')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, f'Успешно редактирахте {self.object.title}.')
        return result


class HikeLevelDeleteView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.DeleteView):
    template_name = 'hike/templates/delete.html'
    permission_required = 'is_staff'
    model = HikeLevel
    success_url = reverse_lazy('hike-level-list')
    extra_context = {
        'cancel_url_button': _('hike level list')
    }

    def form_valid(self, form):
        try:
            messages.success(self.request, f'Успешно изтрихте {self.object.title}.')
            return super().form_valid(form=form)
        except RestrictedError:
            messages.error(self.request, 'За да изтриете това ниво, трябва да изтриете всички походи които го сържат!')
            return HttpResponseRedirect(reverse_lazy('hike-level-delete', kwargs={'pk': self.kwargs.get('pk')}))


class HikeLevelListView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.ListView):
    template_name = 'hike/list-types-or-level.html'
    permission_required = 'is_staff'

    def get_queryset(self):
        return HikeLevel.objects.all()
