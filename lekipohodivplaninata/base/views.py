from django.views import generic as view


class IndexPageTemplateView(view.TemplateView):
    template_name = 'index.html'
