from django.views import generic

from . import forms


class Index(generic.FormView):
    template_name = 'index.html'
    form_class = forms.ExampleForm
