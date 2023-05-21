from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from lekipohodivplaninata.core.mixins import PicturesMixin
from lekipohodivplaninata.hike.forms import HikeForm, HikeCreateForm, HikeUpdateForm, HikeMorePictureUploadForm
from lekipohodivplaninata.hike.models import Hike, HikeMorePicture
from lekipohodivplaninata.users_app.models import BaseProfile, GuideProfile

HikeModel = Hike


class HikeCreateView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.CreateView):
    template_name = 'hike/create-hike.html'
    permission_required = 'is_staff'
    form_class = HikeCreateForm

    def get_success_url(self):
        return reverse_lazy('hike detail', kwargs={
            'pk': self.object.pk,
            'slug': self.object.slug,
        })


class HikeDetailView(views.DetailView):
    template_name = 'hike/detail-hike.html'
    form_class = HikeForm
    model = HikeModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_anonymous:
            context['user'] = self.get_user(self.request)

        context['hikes'] = HikeModel.objects.all()
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
    form_class = HikeUpdateForm
    model = HikeModel

    def get_success_url(self):
        return reverse_lazy('hike detail', kwargs={
            'pk': self.object.pk,
            'slug': self.object.slug,
        })


class HikeMorePictureUpload(PicturesMixin, auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin,
    views.FormView):
    template_name = 'hike/more-pictures-hike.html'
    permission_required = 'is_staff'
    form_class = HikeMorePictureUploadForm
    model = HikeMorePicture

    def get_success_url(self):
        return reverse_lazy('hike detail', kwargs={
            'pk': self.kwargs['pk'],
            'slug': self.kwargs['slug'],
        })

    def form_valid(self, form):
        images = form.files.getlist('picture')
        if images:
            hike = Hike.objects.get(pk=self.kwargs['pk'])
            public_id = hike.main_picture.public_id
            folder = self.get_picture_folder(public_id)
            for image in images:
                url = self.upload_picture(image.file, folder)
                img_id = HikeMorePicture.objects.create(image=url)
                hike.more_pictures.add(img_id)

        return super().form_valid(form=form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = HikeModel.objects.get(pk=self.kwargs['pk'])
        return context


class HikeDeleteView(PicturesMixin, auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin,
    views.DeleteView):
    template_name = 'hike/delete-hike.html'
    success_url = reverse_lazy('hike list')
    permission_required = 'is_staff'
    model = HikeModel

    def form_valid(self, form):
        if self.object.main_picture:
            main_picture_public_id = self.object.main_picture.public_id
            main_picture_folder = self.get_picture_folder(main_picture_public_id)
            self.delete_pictures([main_picture_public_id])
            self.delete_folder(main_picture_folder)

        return super().form_valid(form=form)


class HikeListView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.ListView):
    template_name = 'hike/list-hikes.html'
    permission_required = 'is_staff'
    paginate_by = 2

    def get_queryset(self):
        return HikeModel.objects.all().order_by('event_date')
