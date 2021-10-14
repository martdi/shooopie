from django.shortcuts import render
from django.views.generic import TemplateView

from .models import SiteConfig

class BaseSiteView(TemplateView):
    title = 'Untitled page'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['site'] = SiteConfig.objects.first()
        context['page'] = {
            'title':self.title
        }
        return context

class IndexView(BaseSiteView):
    template_name = 'home.html'
    title = 'Home'