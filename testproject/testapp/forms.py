from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from django_pony_forms.pony_forms import PonyFormMixin


class ExampleTextarea(forms.Textarea):
    renders_label = True

    def render(self, name, value, attrs, label):
        return (
            mark_safe('<label>{0!s}</label>'.format(str(label))) +
            super(ExampleTextarea, self).render(name, value, attrs)
        )


class ExampleForm(PonyFormMixin, forms.Form):
    prefix = 'example'

    name = forms.CharField(max_length=50, required=True, help_text='help text')
    description = forms.CharField(max_length=255, help_text='please fill in a description', widget=ExampleTextarea, required=False)
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

    def update_row_context(self, bound_field):
        return dict(
            widget_name=bound_field.field.widget.__class__.__name__
        )
