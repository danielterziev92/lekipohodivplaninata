from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from lekipohodivplaninata.core.utils import from_cyrillic_to_latin
from lekipohodivplaninata.core.utils import from_str_to_date
from lekipohodivplaninata.hike.forms import HikeCreateForm, HikeDetailForm
from lekipohodivplaninata.hike.models import Hike
from lekipohodivplaninata.users_app.models import BaseProfile
from lekipohodivplaninata.users_app.models import GuideProfile


class HikeCreateView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.CreateView):
    template_name = 'hike/create-hike.html'
    permission_required = 'is_staff'
    form_class = HikeCreateForm

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
        new_path = f'{old_path}/{form.instance.slug}/{form.data["event_date"]}'
        form.base_fields['main_picture'].options['folder'] = new_path

        return form


class HikeDetailView(auth_mixins.LoginRequiredMixin, views.DetailView):
    template_name = 'hike/detail-hike.html'
    permission_required = 'is_staff'
    form_class = HikeDetailForm
    model = Hike

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_user(self.request)
        return context

    @staticmethod
    def get_user(request):
        pk = request.user.pk
        if request.user.is_staff:
            user = GuideProfile.objects.get(pk=pk)
        else:
            user = BaseProfile.objects.get(pk=pk)

        return user


class HikeListView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.ListView):
    template_name = 'hike/list-hikes.html'
    model = Hike
    permission_required = 'is_staff'
