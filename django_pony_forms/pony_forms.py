import six

from django.utils.encoding import force_text

from django.utils.safestring import mark_safe

from django.template.loader import render_to_string
from django.template.context import Context
from django.forms.forms import BoundField, NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy

try:
    # Python >= 2.7
    from collections import OrderedDict
except ImportError:
    from django.utils.datastructures import SortedDict as OrderedDict


class PonyFormMixin(object):
    form_template = 'django_pony_forms/base_form.html'
    row_template = 'django_pony_forms/row.html'
    errorlist_template = 'django_pony_forms/errorlist.html'
    label_template = 'django_pony_forms/label.html'

    fieldset_definitions = dict()
    custom_row_templates = dict()
    required_css_class = 'required'

    def __unicode__(self):
        return render_to_string(
            self.form_template,
            context_instance=self._get_form_context()
        )

    def __str__(self):
        return self.__unicode__()

    def _create_bound_field_dict(self):
        return OrderedDict(
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
        return self._get_form_context()['rows']

    @property
    def hidden_fields(self):
        return self._get_form_context()['hidden_fields']

    @property
    def top_errors(self):
        return self._get_form_context()['top_errors']

    @property
    def fieldsets(self):
        return self._get_form_context()['fieldsets']


class FormContext(Context):
    def __init__(self, form, *args, **kwargs):
        super(FormContext, self).__init__(*args, **kwargs)

        self._form = form

        bound_fields = form._create_bound_field_dict()

        self['hidden_fields'] = self.get_hidden_field_dict(bound_fields)
        self['fields'] = self.get_visible_fields_dict(bound_fields)
        self['rows'] = self.get_rows(self['fields'])
        self['top_errors'] = self.get_top_errors(self['hidden_fields'])
        self['fieldsets'] = FieldsetsContext(form, self['rows'])

    def get_hidden_field_dict(self, bound_fields):
        return RenderableDict(
            (field_name, bound_field)
            for (field_name, bound_field) in six.iteritems(bound_fields) if bound_field.is_hidden
        )

    def get_visible_fields_dict(self, bound_fields):
        return OrderedDict(
            (field_name, bound_field)
            for (field_name, bound_field) in six.iteritems(bound_fields) if not bound_field.is_hidden
        )

    def get_rows(self, visible_fields):
        return RenderableDict(
            (
                field_name,
                RowContext(bound_field, self._form)
            )
            for (field_name, bound_field) in six.iteritems(visible_fields)
        )

    def get_top_errors(self, hidden_fields):
        top_errors = ErrorList(
            self._form.errors.get(NON_FIELD_ERRORS, []),
            self._form.errorlist_template
        )

        for bound_field in six.itervalues(hidden_fields):
            if bound_field.errors:
                top_errors.extend([
                    u'(Hidden field %s) %s' % (bound_field.name, force_text(e)) for e in bound_field.errors
                ])

        return top_errors


class RenderableDict(OrderedDict):
    def __unicode__(self):
        return mark_safe(
            u''.join(
                six.text_type(item) for item in six.itervalues(self)
            )
        )

    def __str__(self):
        return self.__unicode__()


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

    def __str__(self):
        return self.__unicode__()

    def _get_context(self):
        if not hasattr(self, '_context'):
            self._context = self._create_context()
        return self._context

    def _create_context(self):
        label = self._get_label()
        label_tag = self._get_label_tag(label)

        context = dict(
            label=label_tag,
            label_title=label,
            field=self._get_field_string,
            name=self._bound_field.name,
            css_classes=self._bound_field.css_classes(),
            help_text=force_text(self._bound_field.field.help_text or u''),
            errors=self._get_errorlist,
            form=self._form,
            bound_field=self._bound_field,
            must_render_label=self._must_render_label,
        )

        if hasattr(self._form, 'update_row_context'):
            context.update(
                self._form.update_row_context(self._bound_field)
            )

        return context

    def _get_label(self):
        if self._bound_field.label:
            return ugettext_lazy(force_text(self._bound_field.label))
        else:
            return ''

    def _get_label_tag(self, contents):
        bound_field = self._bound_field
        widget = bound_field.field.widget
        id_ = widget.attrs.get('id') or bound_field.auto_id

        if not id_:
            return ''
        else:
            return render_to_string(
                self._form.label_template,
                dict(id=id_, label=contents, field=bound_field.field)
            )

    def _get_field_string(self):
        if self._must_render_label():
            # Default: render boundfield which renders the label and the widget
            result = six.text_type(self._bound_field)
        else:
            # The widget renders its own label
            result = self._render_widget_with_own_label()

        return mark_safe(result)

    def _render_widget_with_own_label(self):
        """
        Render widget. The widget renders its own label
        """
        bound_field = self._bound_field
        widget = bound_field.field.widget

        attrs = bound_field.field.widget_attrs(widget)
        auto_id = bound_field.auto_id

        if auto_id and 'id' not in widget.attrs:
            attrs['id'] = auto_id

        name = bound_field.html_name

        # Render widget widh 'label' attribute
        return widget.render(name, bound_field.value(), attrs=attrs, label=self._get_label())

    def _must_render_label(self):
        """
        Must we render the label?

        Not if the widget has the renders_label property. This means that the widget renders its own label.
        """
        widget = self._bound_field.field.widget

        return not getattr(widget, 'renders_label', False)

    def _get_errorlist(self):
        return ErrorList(self._bound_field.errors, self._form.errorlist_template)

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

    def __str__(self):
        return self.__unicode__()


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
