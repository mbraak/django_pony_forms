[![Travis Status](https://secure.travis-ci.org/mbraak/django_pony_forms.svg)](http://travis-ci.org/mbraak/django_pony_forms) [![Version](https://pypip.in/version/django_pony_forms/badge.svg)](https://pypi.python.org/pypi/django_pony_forms/) [![Development Status](https://pypip.in/status/django_pony_forms/badge.svg)](https://pypi.python.org/pypi/django_pony_forms/)

[![Coverage Status](https://img.shields.io/coveralls/mbraak/django_pony_forms.svg)](https://coveralls.io/r/leukeleu/django_pony_forms) [![Downloads](https://pypip.in/download/django_pony_forms/badge.svg)](https://pypi.python.org/pypi/django_pony_forms/) [![Format](https://pypip.in/format/django_pony_forms/badge.svg)](https://pypi.python.org/pypi/django_pony_forms/) [![Requirements Status](https://requires.io/github/mbraak/django_pony_forms/requirements.png?branch=master)](https://requires.io/github/mbraak/django_pony_forms/requirements/?branch=master)

[![License](https://pypip.in/license/django_pony_forms/badge.svg)](https://pypi.python.org/pypi/django_pony_forms/)  [![Supported Python versions](https://pypip.in/py_versions/django_pony_forms/badge.svg)](https://pypi.python.org/pypi/django_pony_forms/) [![Supported Python implementations](https://pypip.in/implementation/django_pony_forms/badge.svg)](https://pypi.python.org/pypi/django_pony_forms/)

Django pony forms
=================

*Django-pony-forms* helps you to write better html for your Django forms.

Read the documentation on [readthedocs](http://django_pony_forms.readthedocs.org/en/latest/index.html)

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

The package is tested with Django 1.4 - 1.7 and Python 2.6, 2.7, 3.3 and 3.4.

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
