from flask import render_template, render_template_string
from flask_user import login_required
from . import main

@main.route('/')
@login_required
def index():
    return '<h1>Hello World!</h1>'

@main.route('/test/<name>')
@login_required
def test(name):
    return render_template('user.html', name=name)

@main.route('/hhh')
def home_page():
    return render_template_string("""
        {% extends "base.html" %}
        {% block content %}
            <p>{{ url_for('user.logout') }}>
            <p>{{ url_for('user.login') }}>
        {% endblock %}
        """)

# @main.route('/cs_entry', methods=['GET', 'POST'])
# def cs_entry():
#     name = None
#     form = FormControlSystem()
#     if form.validate_on_submit():
#         name = form.name.data
#         form.name.data = ''
#     return render_template('cs_entry.html', form=form, name=name)

