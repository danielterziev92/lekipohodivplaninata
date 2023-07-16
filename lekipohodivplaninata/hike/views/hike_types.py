from django.contrib import messages
from django.db.models import RestrictedError
from django.http import HttpResponseRedirect
from django.views import generic as views
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth import mixins as auth_mixins

from lekipohodivplaninata.hike.forms import HikeTypeForm
from lekipohodivplaninata.hike.models import HikeType


class HikeTypeCreateView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.CreateView):
    template_name = 'hike/templates/create-or-update.html'
    permission_required = 'is_staff'
    form_class = HikeTypeForm
    success_url = reverse_lazy('hike type list')


class HikeTypeUpdateView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.UpdateView):
    template_name = 'hike/templates/create-or-update.html'
    permission_required = 'is_staff'
    form_class = HikeTypeForm
    model = HikeType
    success_url = reverse_lazy('hike type list')


class HikeTypeDeleteView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.DeleteView):
    template_name = 'hike/templates/delete.html'
    model = HikeType
    permission_required = 'is_staff'
    success_url = reverse_lazy('hike type list')
    extra_context = {
        'cancel_url_button': _('hike type list')
    }

    def form_valid(self, form):
        try:
            return super().form_valid(form=form)
        except RestrictedError:
            message = 'За да изтриете този тип, трябва да изтриете всички походи които го сържат!'
            messages.add_message(self.request, messages.ERROR, message)
            return HttpResponseRedirect(reverse_lazy('hike type delete', kwargs={'pk': self.kwargs.get('pk')}))


class HikeTypeListView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.ListView):
    template_name = 'hike/list-types-or-level.html'
    permission_required = 'is_staff'

    def get_queryset(self):
        return HikeType.objects.all()
