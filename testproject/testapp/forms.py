from django import forms
from django.core.exceptions import ValidationError

from django_pony_forms.pony_forms import PonyFormMixin


class ExampleForm(PonyFormMixin, forms.Form):
    name = forms.CharField(max_length=50, required=True, help_text='help text')
    description = forms.CharField(max_length=255, help_text='please fill in a description', widget=forms.Textarea, required=False)
    code = forms.CharField(max_length=15, required=True, widget=forms.HiddenInput)
    example_type = forms.ChoiceField(choices=[(1, 'abc'), (2, 'def')])

    fieldset_definitions = dict(
        f1=['name'],
        f2=['type', 'description']
    )

    row_template = 'foundation_row.html'
    errorlist_template = 'foundation_errorlist.html'

    def clean(self):
        raise ValidationError('Top message')
