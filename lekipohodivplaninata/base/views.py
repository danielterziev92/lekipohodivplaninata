from django.views import generic as views

from lekipohodivplaninata.base.forms import SignUpHikeForm
from lekipohodivplaninata.base.models import SignUpForHike


class IndexPageTemplateView(views.TemplateView):
    template_name = 'index.html'


class SignUpHike(views.CreateView):
    template_name = 'hike/sign-up-for-hike.html'
    model = SignUpForHike
    form_class = SignUpHikeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
