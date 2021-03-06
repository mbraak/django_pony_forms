import unittest

from pyquery import PyQuery as pq

from django import forms
from django.test import Client

from .forms import ExampleForm
from .test_utils import format_list


class PonyFormTest(unittest.TestCase):
    def test_html(self):
        # 1. Form without values
        form = ExampleForm()

        # Wrap html in 'div' so pyquery can parse it
        html = u"<div>{0!s}</div>".format(str(form))
        d = pq(html)

        # Check hidden field
        hidden = d('input[type=hidden]')
        self.assertEqual(len(hidden), 1)
        self.assertEqual(hidden.attr('id'), 'id_example-code')
        self.assertEqual(hidden.attr('name'), 'example-code')

        # There is no errorlist
        errorlist = d('ul.errorlist')
        self.assertEqual(len(errorlist), 0)

        # Form rows
        rows = d('div.form-row')
        self.assertEqual(
            format_list(
                [pq(row).attr('id') for row in rows],
                sort=False
            ),
            'row-example-name row-example-description row-example-example_type'
        )

        # Name row
        name_row = d('div#row-example-name')
        label = name_row.find('label')
        self.assertEqual(label.text(), 'Name TextInput')
        self.assertTrue(name_row.hasClass('required'))

        name_field = d('#id_example-name')
        self.assertEqual(name_field.attr('type'), 'text')
        self.assertEqual(name_field.attr('name'), 'example-name')
        self.assertEqual(name_field.attr('maxlength'), '50')

        help_text = name_row.find('p')
        self.assertEqual(help_text.text(), 'help text')

        # 2. Post form
        form = ExampleForm(dict())

        html = u"<div>{0!s}</div>".format(str(form))
        d = pq(html)

        errorlist = d('div.alert')
        self.assertEqual(
            format_list(
                [pq(error).text() for error in errorlist],
                separator=';', sort=False
            ),
            'Top message;(Hidden field code) This field is required.;This field is required.;This field is required.'
        )

    def test_get_form_properties(self):
        def get_text(v):
            if callable(v):
                return v()
            else:
                return v

        form = ExampleForm()

        # 1. Rows
        self.assertEqual(
            format_list(form.rows.keys(), sort=False),
            'name description example_type'
        )

        # 2. Hidden fields
        self.assertEqual(
            format_list(form.hidden_fields.keys()),
            'code'
        )

        # 3. Top errors
        self.assertEqual(len(form.top_errors), 0)

        # 4. Fieldsets
        self.assertEqual(
            format_list(form.fieldsets['f1'].keys()),
            'name'
        )

        # 5. Iterate rows
        self.assertEqual(
            format_list(
                [
                    pq(str(row)).attr('id') for row in form.rows.values()
                ],
                sort=False
            ),
            'row-example-name row-example-description row-example-example_type'
        )

        # 6. Post form and get top errors
        form = ExampleForm(dict())
        self.assertEqual(
            format_list(form.top_errors, separator=';', sort=False),
            'Top message;(Hidden field code) This field is required.'
        )

        # 7. Get row properties
        name_row = form.rows['name']
        self.assertEqual(name_row.name, 'name')
        self.assertEqual(name_row.label, '<label for="id_example-name">Name</label>')

        rendered_name_input = get_text(name_row.field)
        self.assertTrue(rendered_name_input.startswith('<input '))
        self.assertTrue('name="example-name"' in rendered_name_input)

        self.assertEqual(name_row.css_classes, 'required')
        self.assertEqual(get_text(name_row.help_text), 'help text')
        self.assertEqual(get_text(name_row.errors), ['This field is required.'])

    def test_empty_label(self):
        # setup
        form = ExampleForm()
        form.fields['name'].label = ''

        # 1. Get html
        html = u"<div>{0!s}</div>".format(str(form))
        d = pq(html)

        self.assertEqual(len(d('.row-name label')), 0)

    def test_empty_fieldsets(self):
        # setup
        class FormWithoutFieldsets(ExampleForm):
            name = forms.CharField()

        form = FormWithoutFieldsets()

        # 1. Get fieldsets
        self.assertEqual(form.fieldsets['aa'], None)

    def test_frontpage(self):
        client = Client()

        response = client.get('/')
        d = pq(response.content)

        name_field = d('#id_example-name')
        self.assertEqual(name_field.attr('name'), 'example-name')
