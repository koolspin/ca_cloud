from flask import Flask, render_template

# basedir = os.path.abspath(os.path.dirname(__file__))
#
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{0}'.format(os.path.join(basedir, 'ca_cloud.db'))
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['SECRET_KEY'] = 'b8b94e6e-02af-11e6-9a8a-b7a0d5674e8a'
#
# db = SQLAlchemy(app)
# bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/cs_entry', methods=['GET', 'POST'])
def cs_entry():
    name = None
    form = FormControlSystem()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('cs_entry.html', form=form, name=name)

