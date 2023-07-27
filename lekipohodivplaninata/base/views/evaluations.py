from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.utils.translation import gettext_lazy as _

from lekipohodivplaninata.base.forms import SiteEvaluationForm
from lekipohodivplaninata.base.models import SiteEvaluation


class SiteEvaluationCreateView(views.CreateView):
    template_name = 'evaluation.html'
    form_class = SiteEvaluationForm
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Моля да оцените сайта ни:',
        'action_url': _('site-evaluation')
    }

    def get(self, request, *args, **kwargs):
        if cache.get('is_signed'):
            cache.delete('is_signed')
            return super().get(request, *args, **kwargs)

        return redirect('index')


class SiteEvaluationListView(views.ListView):
    template_name = 'all-site-evaluations.html'
    model = SiteEvaluation
    paginate_by = 10
