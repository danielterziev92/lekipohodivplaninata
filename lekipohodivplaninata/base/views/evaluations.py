from django.core.cache import cache
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views
from django.utils.translation import gettext_lazy as _

from lekipohodivplaninata.base.forms import SiteEvaluationForm, HikeEvaluationForm
from lekipohodivplaninata.base.models import SiteEvaluation, HikeEvaluation


class SiteEvaluationCreateView(views.CreateView):
    template_name = 'evaluation.html'
    form_class = SiteEvaluationForm
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if cache.get('is_signed'):
            cache.delete('is_signed')
            return super().get(request, *args, **kwargs)

        return redirect('index')


class SiteEvaluationListView(views.ListView):
    template_name = 'all-site-evaluations.html'
    model = SiteEvaluation
    paginate_by = 10


class HikeEvaluationDetailView(views.CreateView):
    template_name = 'hike-evaluation.html'
    model = HikeEvaluation
    form_class = HikeEvaluationForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = get_object_or_404(HikeEvaluation, slug=self.kwargs['slug'])
        return context
