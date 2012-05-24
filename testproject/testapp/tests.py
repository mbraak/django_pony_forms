from pyquery import PyQuery as pq

from django.utils import unittest
from django import forms

from forms import ExampleForm
from test_utils import format_list


class PonyFormTest(unittest.TestCase):
    def test_html(self):
        # 1. Form without values
        form = ExampleForm()

        # Wrap html in 'div' so pyquery can parse it
        html = u"<div>%s</div>" % unicode(form)
        d = pq(html)

        # Check hidden field
        hidden = d('input[type=hidden]')
        self.assertEqual(len(hidden), 1)
        self.assertEqual(hidden.attr('id'), 'id_code')
        self.assertEqual(hidden.attr('name'), 'code')

        # There is no errorlist
        errorlist = d('ul.errorlist')
        self.assertEquals(len(errorlist), 0)

        # Form rows
        rows = d('div.form-row')
        self.assertEqual(
            format_list(
                [pq(row).attr('id') for row in rows],
                sort=False
            ),
            'row-name row-description row-type'
        )

        # Name row
        name_row = d('div#row-name')
        label = name_row.find('label')
        self.assertEqual(label.attr('for'), 'id_name')
        self.assertEqual(label.text(), 'Name')
        self.assertTrue(name_row.hasClass('required'))

        name_field = d('#id_name')
        self.assertEqual(name_field.attr('type'), 'text')
        self.assertEqual(name_field.attr('name'), 'name')
        self.assertEqual(name_field.attr('maxlength'), '50')

        help_text = name_row.find('span.helptext')
        self.assertEqual(help_text.text(), 'help text')

        # 2. Post form
        form = ExampleForm(dict())

        html = u"<div>%s</div>" % unicode(form)
        d = pq(html)

        errorlist = d('ul.errorlist')
        self.assertEqual(
            format_list(
                [pq(error).text() for error in errorlist],
                separator=';', sort=False
            ),
            'Top message (Hidden field code) This field is required.;This field is required.;This field is required.'
        )

    def test_get_form_properties(self):
        form = ExampleForm()

        # 1. Rows
        self.assertEqual(
            format_list(form.rows.keys(), sort=False),
            'name description type'
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
                    pq(unicode(row)).attr('id') for row in form.rows
                ],
                sort=False
            ),
            'row-name row-description row-type'
        )

        # 6. Post form and get top errors
        form = ExampleForm(dict())
        self.assertEqual(
            format_list(form.top_errors, separator=';', sort=False),
            'Top message;(Hidden field code) This field is required.'
        )

    def test_empty_label(self):
        # setup
        form = ExampleForm()
        form.fields['name'].label = ''

        # 1. Get html
        html = u"<div>%s</div>" % unicode(form)
        d = pq(html)

        self.assertEqual(len(d('.row-name label')), 0)

    def test_empty_fieldsets(self):
        # setup
        class FormWithoutFieldsets(ExampleForm):
            name = forms.CharField()

        form = FormWithoutFieldsets()

        # 1. Get fieldsets
        self.assertEqual(form.fieldsets['aa'], None)
