from flask import render_template
from . import main

@main.route('/')
def index():
    return '<h1>Hello World!</h1>'

@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

# @main.route('/cs_entry', methods=['GET', 'POST'])
# def cs_entry():
#     name = None
#     form = FormControlSystem()
#     if form.validate_on_submit():
#         name = form.name.data
#         form.name.data = ''
#     return render_template('cs_entry.html', form=form, name=name)

