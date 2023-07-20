from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from lekipohodivplaninata.base.forms import SliderCreateForm, SliderEditForm
from lekipohodivplaninata.base.models import Slider
from lekipohodivplaninata.core.mixins import PicturesMixin


class SliderCreateView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.CreateView):
    permission_required = 'is_staff'
    template_name = 'slider/create.html'
    form_class = SliderCreateForm
    success_url = reverse_lazy('slider-list')


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
    success_url = reverse_lazy('slider-list')


class SliderDeleteView \
            (PicturesMixin, auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.DeleteView):
    permission_required = 'is_staff'
    template_name = 'slider/delete.html'
    model = Slider
    success_url = reverse_lazy('slider-list')

    def form_valid(self, form):
        public_id = self.object.image.public_id
        self.delete_pictures(public_id)
        folder = self.get_picture_folder(public_id=public_id)
        self.delete_folder(folder=folder)

        return super().form_valid(form=form)
