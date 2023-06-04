from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from lekipohodivplaninata.core.mixins import PicturesMixin, UserDataMixin
from lekipohodivplaninata.hike.forms import HikeForm, HikeCreateForm, HikeUpdateForm, HikeMorePictureUploadForm, \
    HikeTypeForm, HikeLevelForm
from lekipohodivplaninata.hike.models import Hike, HikeMorePicture, HikeAdditionalInfo, HikeType, HikeLevel
from lekipohodivplaninata.users_app.models import BaseProfile, GuideProfile

HikeModel = Hike


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


class HikeTypeListView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.ListView):
    template_name = 'hike/list-types-or-level.html'
    permission_required = 'is_staff'

    def get_queryset(self):
        return HikeType.objects.all()


class HikeLevelCreateView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.CreateView):
    template_name = 'hike/templates/create-or-update.html'
    permission_required = 'is_staff'
    form_class = HikeLevelForm
    success_url = reverse_lazy('hike level list')


class HikeLevelUpdateView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.UpdateView):
    template_name = 'hike/templates/create-or-update.html'
    permission_required = 'is_staff'
    form_class = HikeLevelForm
    model = HikeLevel
    success_url = reverse_lazy('hike level list')


class HikeLevelDeleteView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.DeleteView):
    template_name = 'hike/templates/delete.html'
    permission_required = 'is_staff'
    model = HikeLevel
    success_url = reverse_lazy('hike level list')


class HikeLevelListView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.ListView):
    template_name = 'hike/list-types-or-level.html'
    permission_required = 'is_staff'

    def get_queryset(self):
        return HikeLevel.objects.all()


class HikeCreateView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.CreateView):
    template_name = 'hike/create-hike.html'
    permission_required = 'is_staff'
    form_class = HikeCreateForm

    def get_success_url(self):
        return reverse_lazy('hike detail', kwargs={
            'pk': self.object.pk,
            'slug': self.object.slug,
        })


class HikeDetailView(UserDataMixin, views.DetailView):
    template_name = 'hike/detail-hike.html'
    form_class = HikeForm
    model = HikeModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_anonymous:
            context['user'] = self.get_user(self.request)

        context['hikes'] = HikeModel.objects.all()
        return context

    def get_user(self, request):
        pk = request.user.pk
        if request.user.is_staff:
            try:
                user = GuideProfile.objects.get(pk=pk)
            except ObjectDoesNotExist:
                user = self.create_guide_profile()
        else:
            user = BaseProfile.objects.get(pk=pk)

        return user


class HikeUpdateView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.UpdateView):
    template_name = 'hike/update-hike.html'
    permission_required = 'is_staff'
    form_class = HikeUpdateForm
    model = HikeModel

    def get(self, request, *args, **kwargs):

        if issubclass(self.model, HikeModel):
            additional_info = HikeAdditionalInfo.objects.get(hike_id=self.kwargs['pk'])
            for field, value in additional_info.__dict__.items():
                if field in ['_state', 'id', 'hike_id_id']:
                    continue
                self.form_class.declared_fields[field].widget.attrs['value'] = value

        return super().get(request, *args, **kwargs)

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
        public_ids = []
        more_pictures = self.object.more_pictures.all()

        if more_pictures:
            for picture in more_pictures:
                public_ids.append(picture.image.public_id)

        main_picture_public_id = self.object.main_picture.public_id
        public_ids.append(main_picture_public_id)

        self.delete_pictures(public_ids)

        main_picture_folder = self.get_picture_folder(main_picture_public_id)
        self.delete_folder(main_picture_folder)

        HikeAdditionalInfo.objects.get(hike_id=self.object).delete()

        return super().form_valid(form=form)


class HikeListView(UserDataMixin, views.ListView):
    template_name = 'hike/list-hikes.html'
    paginate_by = 10

    def get_queryset(self):
        return HikeModel.objects.all().order_by('event_date')
