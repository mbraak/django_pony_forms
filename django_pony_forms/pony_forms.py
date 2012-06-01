from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.datastructures import SortedDict
from django.template.loader import render_to_string
from django.template.context import Context
from django.forms.forms import BoundField, NON_FIELD_ERRORS


class PonyFormMixin(object):
    form_template = 'django_pony_forms/base_form.html'
    row_template = 'django_pony_forms/row.html'
    errorlist_template = 'django_pony_forms/errorlist.html'

    fieldset_definitions = dict()
    custom_row_templates = dict()
    required_css_class = 'required'

    def __unicode__(self):
        return render_to_string(
            self.form_template,
            context_instance=self._get_form_context()
        )

    def _create_bound_field_dict(self):
        return SortedDict(
            (field_name, BoundField(self, field, field_name))
            for (field_name, field) in self.fields.items()
        )

    def _get_form_context(self):
        if not hasattr(self, '_form_context'):
            self._form_context = FormContext(self)
        return self._form_context

    def _get_row_template_name(self, field_name):
        return self.custom_row_templates.get(field_name, self.row_template)
    
    @property
    def rows(self):
        return self._get_form_context().rows

    @property
    def hidden_fields(self):
        return self._get_form_context().hidden_fields

    @property
    def top_errors(self):
        return self._get_form_context().top_errors

    @property
    def fieldsets(self):
        return self._get_form_context().fieldsets


class BootstrapFormMixin(PonyFormMixin):
    form_template = 'django_pony_forms/bootstrap_form.html'
    row_template = 'django_pony_forms/bootstrap_row.html'


class FormContext(Context):
    def __init__(self, form, *args, **kwargs):
        super(FormContext, self).__init__(*args, **kwargs)

        self._form = form

        bound_fields = form._create_bound_field_dict()

        self.hidden_fields = self.get_hidden_field_dict(bound_fields)
        self.fields = self.get_visible_fields_dict(bound_fields)
        self.rows = self.get_rows(self.fields)
        self.top_errors = self.get_top_errors(self.hidden_fields)
        self.fieldsets = FieldsetsContext(form, self.rows)

    def get_hidden_field_dict(self, bound_fields):
        return RenderableDict(
            (field_name, bound_field)
            for (field_name, bound_field) in bound_fields.iteritems() if bound_field.is_hidden
        )

    def get_visible_fields_dict(self, bound_fields):
        return SortedDict(
            (field_name, bound_field)
            for (field_name, bound_field) in bound_fields.iteritems() if not bound_field.is_hidden
        )

    def get_rows(self, visible_fields):
        return RenderableDict(
            (
                field_name,
                RowContext(bound_field, self._form)
            )
            for (field_name, bound_field) in visible_fields.iteritems()
        )

    def get_top_errors(self, hidden_fields):
        top_errors = ErrorList(
            self._form.errors.get(NON_FIELD_ERRORS, []),
            self._form.errorlist_template
        )

        for bound_field in hidden_fields.itervalues():
            if bound_field.errors:
                top_errors.extend([
                    u'(Hidden field %s) %s' % (bound_field.name, force_unicode(e)) for e in bound_field.errors
                ])

        return top_errors


class RenderableDict(SortedDict):
    def __unicode__(self):
        return mark_safe(
            u''.join(
                unicode(item) for item in self.itervalues()
            )
        )

    def __iter__(self):
        return self.itervalues()


class RowContext(object):
    def __init__(self, bound_field, form):
        super(RowContext, self).__init__()

        self._bound_field = bound_field
        self._form = form

    def __unicode__(self):
        template_name = self._form._get_row_template_name(self._bound_field.name)

        return mark_safe(
            render_to_string(template_name, self._get_context())
        )

    def _get_context(self):
        if not hasattr(self, '_context'):
            self._context = self._create_context()
        return self._context

    def _create_context(self):
        if not self._bound_field.label:
            label_tag = ''
        else:
            label = force_unicode(self._bound_field.label)
            label_tag = self._bound_field.label_tag(label) or ''

        return dict(
            label=label_tag,
            field=unicode(self._bound_field),
            name=self._bound_field.name,
            css_classes=self._bound_field.css_classes(),
            help_text=force_unicode(self._bound_field.field.help_text or u''),
            errors=ErrorList(self._bound_field.errors, self._form.errorlist_template),
        )

    @property
    def name(self):
        return self._bound_field.name

    @property
    def label(self):
        return self._get_context()['label']

    @property
    def field(self):
        return self._get_context()['field']

    @property
    def css_classes(self):
        return self._get_context()['css_classes']

    @property
    def help_text(self):
        return self._get_context()['help_text']

    @property
    def errors(self):
        return self._get_context()['errors']


class ErrorList(list):
    def __init__(self, errors, errorlist_template):
        super(ErrorList, self).__init__(errors)

        self.errorlist_template = errorlist_template

    def __unicode__(self):
        return render_to_string(
            self.errorlist_template,
            dict(errors=self)
        )


class FieldsetsContext(object):
    def __init__(self, form, rows):
        self._form = form
        self._rows = rows

    def __getitem__(self, key):
        field_names = self._form.fieldset_definitions.get(key)
        if not field_names:
            return None
        else:
            rows = [
                self._rows[field_name]
                for field_name in field_names if field_name in self._rows
            ]

            return RenderableDict(
                (row.name, row) for row in rows
            )
