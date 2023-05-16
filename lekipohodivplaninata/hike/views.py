from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from lekipohodivplaninata.core.utils import from_cyrillic_to_latin
from lekipohodivplaninata.core.utils import from_str_to_date
from lekipohodivplaninata.hike.forms import HikeForm
from lekipohodivplaninata.hike.models import Hike
from lekipohodivplaninata.users_app.models import BaseProfile
from lekipohodivplaninata.users_app.models import GuideProfile


class HikeCreateView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.CreateView):
    template_name = 'hike/create-hike.html'
    permission_required = 'is_staff'
    form_class = HikeForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        if self.request.method.lower() == 'post':
            self.generate_slug_field(form)
            self.change_path_of_main_picture(form)

        return form

    def get_success_url(self):
        return reverse_lazy('hike detail', kwargs={
            'pk': self.object.pk,
            'slug': self.object.slug,
        })

    @staticmethod
    def generate_slug_field(form):
        slug_prefix = slugify(from_cyrillic_to_latin(form.data["title"]))
        slug_suffix = from_str_to_date(form.data["event_date"])
        form.instance.slug = f'{slug_prefix}-{slug_suffix}'

        return form

    @staticmethod
    def change_path_of_main_picture(form):
        old_path = form.base_fields['main_picture'].options['folder']
        new_path = f'{old_path}/{form.instance.slug}'
        form.base_fields['main_picture'].options['folder'] = new_path

        return form


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


class HikeUpdateView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.UpdateView):
    template_name = 'hike/update-hike.html'
    permission_required = 'is_staff'
    form_class = HikeForm
    model = Hike


class HikeDeleteView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.DetailView):
    template_name = 'hike/delete-hike.html'
    success_url = reverse_lazy('hike list')


class HikeListView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.ListView):
    template_name = 'hike/list-hikes.html'
    permission_required = 'is_staff'
    paginate_by = 2

    def get_queryset(self):
        return Hike.objects.all().order_by('event_date')
