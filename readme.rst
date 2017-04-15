Django pony forms
=================

*Django-pony-forms* helps you to write better html for your Django
forms.

Read the documentation on `readthedocs`_

**1: Better form html by default**

The form html that Django produces is not very nice or useful. For
example, the default output of a Django form is a table.

Just mixin **PonyFormMixin** to produce better html:

.. code:: python

    class ExampleForm(PonyFormMixin, forms.Form):
        name = forms.CharField()

This produces the following html:

.. code:: html

    <div class="form-row row-name">
        <label for="id_name">Name</label>
        <input type="text" id="id_name" name="name" />
    </div>

**2: Write your own form templates**

You can also write your own form templates:

.. code:: python

    class ExampleForm(PonyFormMixin, forms.Form):
        name = forms.CharField()

        form_template = 'my_form.html'
        row_template = 'my_row.html'

my\_form.html:

.. code:: html

    <div class="my_form">
        {{ hidden_fields }}
        {{ top_errors }}
        {{ rows }}
    </div>

Requirements
------------

The package is tested with Django 1.8 - 1.11 and Python 2.7, 3.3-3.6.

Installation
------------

Install the package:

::

    $ pip install django_pony_forms

Add **django\_pony\_forms** to your installed apps in **settings.py**.

.. code:: python

    INSTALLED_APPS = (
        ..
        'django_pony_forms',
    )

.. _readthedocs: http://django_pony_forms.readthedocs.io/en/latest/index.html
