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

        self.form = form

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
                RowContext(bound_field, self.form)
            )
            for (field_name, bound_field) in visible_fields.iteritems()
        )

    def get_top_errors(self, hidden_fields):
        top_errors = ErrorList(
            self.form.errors.get(NON_FIELD_ERRORS, []),
            self.form.errorlist_template
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

        self.bound_field = bound_field
        self.form = form

    def __unicode__(self):
        if not self.bound_field.label:
            label_tag = ''
        else:
            label = force_unicode(self.bound_field.label)
            label_tag = self.bound_field.label_tag(label) or ''

        context = dict(
            label=label_tag,
            field=unicode(self.bound_field),
            name=self.bound_field.name,
            css_classes=self.bound_field.css_classes(),
            help_text=force_unicode(self.bound_field.field.help_text or u''),
            errors=ErrorList(self.bound_field.errors, self.form.errorlist_template),
        )

        return mark_safe(
            render_to_string(self.form.row_template, context)
        )


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
        self.form = form
        self.rows = rows

    def __getitem__(self, key):
        field_names = self.get_fieldset(key)
        if not field_names:
            return None
        else:
            rows = [
                self.rows[field_name]
                for field_name in field_names if field_name in self.rows
            ]

            return RenderableDict(
                (row.bound_field.name, row) for row in rows
            )

    def get_fieldset(self, key):
        if hasattr(self.form, 'fieldset_definitions'):
            return self.form.fieldset_definitions.get(key)
        else:
            return None
