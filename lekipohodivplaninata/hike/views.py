import cloudinary.uploader
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from lekipohodivplaninata.core.mixins import GetHikeForm
from lekipohodivplaninata.hike.forms import HikeForm
from lekipohodivplaninata.hike.models import Hike
from lekipohodivplaninata.users_app.models import BaseProfile, GuideProfile


class HikeCreateView(GetHikeForm, auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin,
    views.CreateView):
    template_name = 'hike/create-hike.html'
    permission_required = 'is_staff'
    form_class = HikeForm

    def get_success_url(self):
        return reverse_lazy('hike detail', kwargs={
            'pk': self.object.pk,
            'slug': self.object.slug,
        })


class HikeDetailView(views.DetailView):
    template_name = 'hike/detail-hike.html'
    form_class = HikeForm
    model = Hike

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_anonymous:
            context['user'] = self.get_user(self.request)

        context['hikes'] = Hike.objects.all()
        return context

    @staticmethod
    def get_user(request):
        pk = request.user.pk
        if request.user.is_staff:
            user = GuideProfile.objects.get(pk=pk)
        else:
            user = BaseProfile.objects.get(pk=pk)

        return user


class HikeUpdateView(GetHikeForm, auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin,
    views.UpdateView):
    template_name = 'hike/update-hike.html'
    permission_required = 'is_staff'
    form_class = HikeForm
    model = Hike

    def get_success_url(self):
        return reverse_lazy('hike detail', kwargs={
            'pk': self.object.pk,
            'slug': self.object.slug,
        })


class HikeDeleteView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.DeleteView):
    template_name = 'hike/delete-hike.html'
    success_url = reverse_lazy('hike list')
    permission_required = 'is_staff'
    model = Hike

    def form_valid(self, form):
        cloudinary.uploader.destroy(self.object.main_picture.public_id)
        return super().form_valid(form=form)


class HikeListView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.ListView):
    template_name = 'hike/list-hikes.html'
    permission_required = 'is_staff'
    paginate_by = 2

    def get_queryset(self):
        return Hike.objects.all().order_by('event_date')
