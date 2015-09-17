from collections import OrderedDict

try:
    # python 3
    from functools import lru_cache
except ImportError:
    # python 2
    from backports.functools_lru_cache import lru_cache

import six

import django
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.template.context import Context
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy
from django.utils.encoding import python_2_unicode_compatible
from django.template.loader import get_template
from django.utils.functional import cached_property

try:
    # django 1.9+
    from django.forms.boundfield import BoundField
except:
    # django 1.7 and 1.8
    from django.forms.forms import BoundField


@python_2_unicode_compatible
class PonyFormMixin(object):
    form_template = 'django_pony_forms/base_form.html'
    row_template = 'django_pony_forms/row.html'
    errorlist_template = 'django_pony_forms/errorlist.html'
    label_template = 'django_pony_forms/label.html'

    fieldset_definitions = dict()
    custom_row_templates = dict()
    required_css_class = 'required'

    def __str__(self):
        template = self._get_template_by_name(self.form_template)

        return mark_safe(
            render_template(template, self._form_context_dict)
        )

    @cached_property
    def _form_context_dict(self):
        return FormContext(self).create_dict()

    def _get_row_template_name(self, field_name):
        return self.custom_row_templates.get(field_name, self.row_template)

    @lru_cache()
    def _get_template_by_name(self, template_name):
        if django.VERSION < (1, 8):
            return get_template(template_name)
        else:
            template_engine = getattr(self, 'template_engine', None)

            return get_template(template_name, using=template_engine)

    @property
    def rows(self):
        return self._form_context_dict['rows']

    @property
    def hidden_fields(self):
        return self._form_context_dict['hidden_fields']

    @property
    def top_errors(self):
        return self._form_context_dict['top_errors']

    @property
    def fieldsets(self):
        return self._form_context_dict['fieldsets']


class FormContext(object):
    def __init__(self, form):
        self.form = form

    def create_dict(self):
        return dict(
            hidden_fields=self.hidden_field_dict,
            fields=self.visible_fields_dict,
            rows=self.rows,
            top_errors=self.top_errors,
            fieldsets=self.fieldsets
        )

    @cached_property
    def bound_field_dict(self):
        return OrderedDict(
            (field_name, BoundField(self.form, field, field_name))
            for (field_name, field) in self.form.fields.items()
        )

    @cached_property
    def hidden_field_dict(self):
        return RenderableDict(
            (field_name, bound_field)
            for (field_name, bound_field) in six.iteritems(self.bound_field_dict) if bound_field.is_hidden
        )

    @cached_property
    def visible_fields_dict(self):
        return OrderedDict(
            (field_name, bound_field)
            for (field_name, bound_field) in six.iteritems(self.bound_field_dict) if not bound_field.is_hidden
        )

    @cached_property
    def rows(self):
        return RenderableDict(
            (
                field_name,
                RowContext(bound_field, self.form)
            )
            for (field_name, bound_field) in six.iteritems(self.visible_fields_dict)
        )

    @cached_property
    def top_errors(self):
        top_errors = ErrorList(
            self.form.errors.get(NON_FIELD_ERRORS, []),
            self.form
        )

        for bound_field in six.itervalues(self.hidden_field_dict):
            if bound_field.errors:
                top_errors.extend([
                    u'(Hidden field %s) %s' % (bound_field.name, force_text(e)) for e in bound_field.errors
                ])

        return top_errors

    @cached_property
    def fieldsets(self):
        return FieldsetsContext(self.form, self.rows)


@python_2_unicode_compatible
class RenderableDict(OrderedDict):
    def __str__(self):
        return mark_safe(
            u''.join(
                six.text_type(item) for item in six.itervalues(self)
            )
        )


@python_2_unicode_compatible
class RowContext(object):
    def __init__(self, bound_field, form):
        super(RowContext, self).__init__()

        self._bound_field = bound_field
        self._form = form

    def __str__(self):
        template_name = self._form._get_row_template_name(self._bound_field.name)
        template = self._form._get_template_by_name(template_name)

        return mark_safe(
            render_template(template, self._context)
        )

    @cached_property
    def _context(self):
        label = self._get_label()
        label_tag = self._get_label_tag(label)

        context = dict(
            label=label_tag,
            label_title=label,
            field=self.field_string,
            name=self._bound_field.name,
            css_classes=self._bound_field.css_classes(),
            help_text=force_text(self._bound_field.field.help_text or u''),
            errors=self.errorlist,
            form=self._form,
            bound_field=self._bound_field,
            must_render_label=self.must_render_label,
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
            template = self._form._get_template_by_name(self._form.label_template)

            return render_template(
                template,
                dict(id=id_, label=contents, field=bound_field.field)
            )

    @cached_property
    def field_string(self):
        if self.must_render_label:
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

    @cached_property
    def must_render_label(self):
        """
        Must we render the label?

        Not if the widget has the renders_label property. This means that the widget renders its own label.
        """
        widget = self._bound_field.field.widget

        return not getattr(widget, 'renders_label', False)

    @cached_property
    def errorlist(self):
        return ErrorList(self._bound_field.errors, self._form)

    @property
    def name(self):
        return self._bound_field.name

    @property
    def label(self):
        return self._context['label']

    @property
    def field(self):
        return self._context['field']

    @property
    def css_classes(self):
        return self._context['css_classes']

    @property
    def help_text(self):
        return self._context['help_text']

    @property
    def errors(self):
        return self._context['errors']


@python_2_unicode_compatible
class ErrorList(list):
    def __init__(self, errors, form):
        super(ErrorList, self).__init__(errors)

        self._form = form

    def __str__(self):
        template = self._form._get_template_by_name(self._form.errorlist_template)

        return render_template(template, dict(errors=self))


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


def render_template(template, context_dict):
    if django.VERSION < (1, 8):
        return template.render(
            Context(context_dict)
        )
    else:
        return template.render(context_dict)
