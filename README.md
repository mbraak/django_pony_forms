[![Travis Status](https://secure.travis-ci.org/mbraak/django_pony_forms.png)](http://travis-ci.org/mbraak/django_pony_forms)

[![Coverage Status](https://coveralls.io/repos/mbraak/django_pony_forms/badge.png?branch=master)](https://coveralls.io/r/mbraak/django_pony_forms)

[![Downloads](https://pypip.in/d/django_pony_forms/badge.png)](https://pypi.python.org/pypi/django_pony_forms/)

[![Downloads](https://pypip.in/v/django_pony_forms/badge.png)](https://pypi.python.org/pypi/django_pony_forms/)

[![Violations](https://goo.gl/M5MZ82)](http://coviolations.io/projects/mbraak/django_pony_forms/)

Django pony forms
=================

*Django-pony-forms* helps you to write better html for your Django forms.

Read the documentation on [readthedocs](http://django_pony_forms.readthedocs.org/en/latest/index.html)

**1: Better form html by default**

The form html that Django produces is not very nice or useful. For example, the default output of a Django form is a table.

Just mixin **PonyFormMixin** to produce better html:

    class ExampleForm(PonyFormMixin, forms.Form):
        name = forms.CharField()

This produces the following html:

    <div class="form-row row-name">
        <label for="id_name">Name</label>
        <input type="text" id="id_name" name="name" />
    </div>

**2: Write your own form templates**

You can also write your own form templates:

    class ExampleForm(PonyFormMixin, forms.Form):
        name = forms.CharField()

        form_template = 'my_form.html'
        row_template = 'my_row.html'

my_form.html:

    <div class="my_form">
        {{ hidden_fields }}
        {{ top_errors }}
        {{ rows }}
    </div>


Requirements
------------

The package is tested with Django 1.3.7, 1.4.5 and 1.5.2.

Installation
------------

Install the package:

    $ pip install django_pony_forms

Add **django_pony_forms** to your installed apps in **settings.py**.

    INSTALLED_APPS = (
        ..
        'django_pony_forms',
    )
