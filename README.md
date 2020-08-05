[![Build Status](https://travis-ci.org/mbraak/django_pony_forms.svg?branch=master)](https://travis-ci.org/mbraak/django_pony_forms) [![Version](https://badge.fury.io/py/django-pony-forms.svg)](https://pypi.python.org/pypi/django-pony-forms/)

[![Coverage Status](https://img.shields.io/coveralls/mbraak/django_pony_forms.svg)](https://coveralls.io/r/mbraak/django_pony_forms?branch=master)
[![Requirements Status](https://requires.io/github/mbraak/django_pony_forms/requirements.svg?branch=master)](https://requires.io/github/mbraak/django_pony_forms/requirements/?branch=master)

[![License](https://img.shields.io/pypi/l/django_pony_forms.svg)](https://pypi.python.org/pypi/django_pony_forms/)

Django pony forms
=================

*Django-pony-forms* helps you to write better html for your Django forms.

Read the documentation on [readthedocs](http://django_pony_forms.readthedocs.io/en/latest/index.html)

**1: Better form html by default**

The form html that Django produces is not very nice or useful. For example, the default output of a Django form is a table.

Just mixin **PonyFormMixin** to produce better html:

```python
class ExampleForm(PonyFormMixin, forms.Form):
    name = forms.CharField()
```

This produces the following html:

```html
<div class="form-row row-name">
    <label for="id_name">Name</label>
    <input type="text" id="id_name" name="name" />
</div>
```

**2: Write your own form templates**

You can also write your own form templates:

```python
class ExampleForm(PonyFormMixin, forms.Form):
    name = forms.CharField()

    form_template = 'my_form.html'
    row_template = 'my_row.html'
```

my_form.html:

```html
<div class="my_form">
    {{ hidden_fields }}
    {{ top_errors }}
    {{ rows }}
</div>
```

Requirements
------------

The package is tested with Django 2.2 - 3.1 and Python 3.6 - 3.8.

Installation
------------

Install the package:

```
$ pip install django_pony_forms
```

Add **django_pony_forms** to your installed apps in **settings.py**.

```python
INSTALLED_APPS = (
    ..
    'django_pony_forms',
)
```
