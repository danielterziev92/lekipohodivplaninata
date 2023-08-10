from django.contrib.auth import get_user_model
from django.contrib.auth import mixins
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic as views

from lekipohodivplaninata.core.mixins import UserFormMixin
from lekipohodivplaninata.users_app.forms import GuideProfileFormUser, BaseUserUpdateForm
from lekipohodivplaninata.users_app.models import BaseProfile

UserModel = get_user_model()


class UserDetailView(UserFormMixin, mixins.LoginRequiredMixin, views.DetailView):
    template_name = 'users/detail-user.html'
    success_url = reverse_lazy('user-detail')

    @property
    def model(self):
        return self.get_model()


class UserUpdateInformation(UserFormMixin, mixins.LoginRequiredMixin, views.UpdateView):
    template_name = 'users/edit-user.html'

    def get_success_url(self):
        return reverse_lazy('user-detail', kwargs={
            'pk': self.request.user.pk,
        })

    def get_form_class(self):
        if self.request.user.is_staff:
            return GuideProfileFormUser

        return BaseUserUpdateForm

    @property
    def model(self):
        return self.get_model()

    @property
    def fields(self):
        return self.get_fields_form('first_name', 'last_name')


class UserDeleteView(UserFormMixin, mixins.LoginRequiredMixin, views.DeleteView):
    template_name = 'users/delete-user.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        pk = self.object.pk
        super().form_valid(form)

        if self.request.user.is_staff:
            BaseProfile.objects.get(pk=pk).delete()

        UserModel.objects.get(pk=pk).delete()
        return HttpResponseRedirect(self.success_url)

    @property
    def model(self):
        return self.get_model()
