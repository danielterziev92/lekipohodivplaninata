from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import mixins
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic as views

from lekipohodivplaninata.api_app.models import Subscribe
from lekipohodivplaninata.core.mixins import UserFormMixin
from lekipohodivplaninata.users_app.forms import GuideProfileFormUser, BaseUserUpdateForm
from lekipohodivplaninata.users_app.models import BaseProfile

UserModel = get_user_model()


class UserDetailView(UserFormMixin, mixins.LoginRequiredMixin, views.DetailView):
    template_name = 'users/detail-user.html'
    success_url = reverse_lazy('user-detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_email = context.get('object').get_email
        context['is_subscribed'] = self.is_user_subscribed(user_email)
        if context['is_subscribed']:
            context['unsubscribed_slug'] = self.get_unsubscribe_url(user_email)
        return context

    @property
    def model(self):
        return self.get_model()

    @staticmethod
    def is_user_subscribed(email):
        obj = Subscribe.objects.filter(email=email).first()
        if obj:
            return True if obj.is_active else False

        return False

    @staticmethod
    def get_unsubscribe_url(email):
        return Subscribe.objects.filter(email=email).get().slug_to_unsubscribe


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

    def form_valid(self, form):
        messages.success(self.request, 'Успешно редактирахте профила си.')
        return super().form_valid(form)

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

        messages.success(self.request, 'Успешно изтрихте профила си.')
        return HttpResponseRedirect(self.success_url)

    @property
    def model(self):
        return self.get_model()
