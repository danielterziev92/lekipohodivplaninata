from django.views import generic as views
from django.urls import reverse_lazy
from django.contrib.auth import mixins as auth_mixins

from lekipohodivplaninata.core.mixins import PicturesMixin
from lekipohodivplaninata.hike.forms import HikeMorePictureUploadForm
from lekipohodivplaninata.hike.models import Hike, HikeMorePicture

HikeModel = Hike


class HikeMorePictureCreate \
            (PicturesMixin, auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.FormView):
    template_name = 'hike/more-picture/more-pictures-hike-add.html'
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


class HikeMorePictureListView \
            (PicturesMixin, auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.ListView):
    template_name = 'hike/more-picture/more-pictures-hike-list.html'
    permission_required = 'is_staff'
    model = HikeMorePicture

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hike_object = None

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['hike_object'] = self.hike_object
        return context_data

    def get_queryset(self):
        self.hike_object = Hike.objects.filter(slug=self.kwargs['slug']).first()
        return self.hike_object.more_pictures.all()


class HikeMorePictureDeleteView \
            (PicturesMixin, auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.DeleteView):
    template_name = 'hike/more-picture/more-pictures-hike-delete.html'
    permission_required = 'is_staff'
    model = HikeMorePicture

    def get_success_url(self):
        return reverse_lazy('hike more pictures list', kwargs={
            'slug': self.kwargs['slug']
        })

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object'] = HikeMorePicture.objects.filter(pk=self.kwargs['pk']).first()
        context_data['hike_object'] = Hike.objects.filter(slug=self.kwargs['slug']).first()
        return context_data

    def form_valid(self, form):
        self.delete_pictures(self.object.image.public_id)
        return super().form_valid(form=form)
