

# QDCrumbs
## Quick & Dirty Breadcrumbs

## Description
This package provides a simple way to add dynamic breadcrumbs to a Flask application. The breadcrumbs can easily be used in a jinja2 template.

QDcrumbs work in both the main Flask application and in Flask Blueprints, and currently support a single variable page, simply import qdcrumb from qdcrumbs and follow the examples below.

## Get started:
Getting started with qdcrumbs is easy! Import the qdcrumb object (from qdcrumbs import qdcrumb) and follow the example below.

### Examples
The following examples work both in the main Flask app and Blueprints!

Importing qdcrumbs:
```python
from flask import Flask
from qdcrumbs import qdcrumb
```

Standard Usage:
```python
    @app.route('/')
    def my_page():
        x = qdcrumb.get_crumbs()
        return render_template('/my_page.html', breadcrumbs=x)
```
With a variable name:
```python 
    @app.route('/path/to/<var>')
    def my_page(var):
        x = qdcrumb.get_crumbs(var)
        return render_template(f'/path/to/{var}.html', breadcrumbs=x)
```
### IMPORTANT!
qdcrumb.get_crumbs() must be called from within a function that points to a resource's route: i.e. a function with the route decorator (@app.route | @blueprint.route). This is because the url is resolved via Flask using url_for() which takes the name of the function that was decorated.

Breadcrumbs are provided as a list of the Breadcrumb class and have the following attributes:

- url     -->     Path to the current page/resource & preceding pages.
- text    -->     Name of the current page/resource.

The breadcrumbs do not provide the site's root directory, this can be added manually trivially (see html jinja2 template example below).

```html
<div>
    <!--
        Include a static link to the site root (Index.html)
        (The Application's root must be added manually)
    -->
    <a href="{{ url_for('index.html')}}">Index</a>

    <!--Loop through the breadcrumbs to this resource-->
    {%- for breadcrumb in breadcrumbs -%}
        <a href="{{ breadcrumb.url }}"> / {{ breadcrumb.text }}</a>
    {%- endfor -%}

</div>
```