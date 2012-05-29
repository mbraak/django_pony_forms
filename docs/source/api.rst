Api
===

PonyFormMixin
-------------

PonyFormMixin has the following properties: 

form_template
^^^^^^^^^^^^^

This sets the form template. The default is 'django_pony_forms/base_form.html'.

::

    class ExampleForm(PonyFormMixin, forms.Form):
        form_template = 'my_form.html'

row_template
^^^^^^^^^^^^

This sets the row template. The default is 'django_pony_forms/row.html'.

::

    class ExampleForm(PonyFormMixin, forms.Form):
        row_template = 'my_row.html'

errorlist_template
^^^^^^^^^^^^^^^^^^

This sets the errorlist template. The default is 'django_pony_forms/errorlist.html'.

::

    class ExampleForm(PonyFormMixin, forms.Form):
        errorlist_template = 'my_errorlist.html'


fieldset_definitions
^^^^^^^^^^^^^^^^^^^^

This defines the fieldsets that you can use in your view template. It is a dictionary of lists of fieldnames:

.. code-block:: python

    class ExampleForm(PonyFormMixin, forms.Form):
        fieldset_definitions = dict(
            first=['field_a', 'field_b']
            another=['field_x', 'field_y']
        )

The referenced fields must exist in the form.

View template:

.. code-block:: html+django

    {{ form.fieldsets.first }}

Context for form template
-------------------------

In your form template you can use the following variables.

hidden_fields
^^^^^^^^^^^^^

Renders the hidden fields. You can also access individual hidden fields.

To render all hidden fields:

.. code-block:: html+django

    {{ hidden_fields }}

To render a single hidden field:

.. code-block:: html+django

    {{ hidden_field.my_hidden_field }}

fields
^^^^^^

This is a dictionary of all the bound fields. It renders a widget.

.. code-block:: html+django

    {{ field.my_name }}

rows
^^^^

Renders all the rows. You can also access individual rows.

To render all rows:

.. code-block:: html+django

    {{ rows }}

To render a single row. This renders the full row including label and widget.

.. code-block:: html+django

    {{ row.my_name }}

top_errors
^^^^^^^^^^

This renders all top errors. You can also iterate over the errors.

.. code-block:: html+django

    {{ top_errors }}


To iterate over the errors:

.. code-block:: html+django

    {% for error in top_errors %}
        <p>{{ errors }}</p>
    {% endfor %}

fieldsets
^^^^^^^^^

You can use this to render a specific fieldset.

.. code-block:: html+django

    {{ form.fieldsets.my_first_fieldset }}

Context for row template
------------------------

In a row template you can use the following variables:

label
^^^^^

This renders the label tag:

.. code-block:: html+django

    {{ label }}

field
^^^^^

This renders the widget:

.. code-block:: html+django

    {{ field }}

name
^^^^

This is the name of the field:

.. code-block:: html+django

    {{ name }}

css_classes
^^^^^^^^^^^

This contains the css classes that are defined by Django. For example, the 'required' class.

.. code-block:: html+django

    <div{% if css_classes %} class="{{ css_classes }}"{% endif %}>
    </div>

help_text
^^^^^^^^^

This defines the help text.

.. code-block:: html+django

    {{ help_text }}

errors
^^^^^^

This renders the errors. You can also iterate over the errors.

.. code-block:: html+django

    {{ errors }}

To iterate over the errors:

.. code-block:: html+django

    {% for error in errors %}
        {{ error }}
    {% endfor %}
