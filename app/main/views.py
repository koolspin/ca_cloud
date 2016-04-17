import uuid
import os
import shutil
from flask import render_template, render_template_string, request, redirect, url_for
from flask.ext.login import current_user
from flask_user import login_required
from werkzeug.utils import secure_filename
from . import main
from .forms import FormControlSystem, FormCsDelete, FileUpload
from ..models import ControlSystem
from .. import db

@main.route('/')
@login_required
def index():
    return '<h1>Hello World!</h1>'

@main.route('/test/<name>')
@login_required
def test(name):
    return render_template('user.html', name=name)

@main.route('/cs')
@login_required
def cs_list():
    xid = int(current_user.get_id())
    cs = ControlSystem.query.filter_by(user_id=xid).order_by(ControlSystem.cs_name).all()
    return render_template('cs_list.html', cs_collection=cs)

@main.route('/cs_entry/<csid>', methods=['GET', 'POST'])
@login_required
def cs_entry(csid):
    form = FormControlSystem()
    xid = int(current_user.get_id())
    if request.method == 'POST':
        if form.validate_on_submit():
            if len(form.user_pw.data) > 0 and form.user_pw.data != form.user_pw2.data:
                return
            cs = None
            temp_id = int(form.cs_id.data)
            if temp_id > 0:
                cs = ControlSystem.query.filter_by(id=temp_id, user_id=xid).first()
                cs.id = temp_id
            if cs is None:
                cs = ControlSystem()
                temp_id = 0
                cs.cs_uuid = str(uuid.uuid4())
            cs.user_id = xid
            cs.cs_name = form.name.data
            cs.cs_ipid = form.ipid.data
            cs.ssl_flag = form.ssl_on.data
            cs.user_name = form.user_id.data
            cs.user_pw = form.user_pw.data
            cs.addr1_host = form.addr1_host_name.data
            cs.addr1_cip_port = form.addr1_port_num.data
            cs.addr2_host = form.addr2_host_name.data
            cs.addr2_cip_port = form.addr2_port_num.data
            if temp_id == 0:
                db.session.add(cs)
                create_project_folders(cs.cs_uuid)
            db.session.commit()
    if request.method == 'GET':
        csi = int(csid)
        cs = ControlSystem.query.filter_by(id=csi, user_id=xid).first()
        if cs is not None:
            form.cs_id.data = str(csi)
            form.name.data = cs.cs_name
            form.ipid.data = cs.cs_ipid
            form.ssl_on.data = cs.ssl_flag
            form.user_id.data = cs.user_name
            form.user_pw.data = cs.user_pw
            form.user_pw2.data = cs.user_pw
            form.addr1_host_name.data = cs.addr1_host
            form.addr1_port_num.data = cs.addr1_cip_port
            form.addr2_host_name.data = cs.addr2_host
            form.addr2_port_num.data = cs.addr2_cip_port
        else:
            form.cs_id.data = str(0)
            form.name.data = ''
            form.ipid.data = 3
            form.ssl_on.data = False
            form.user_id.data = ''
            form.user_pw.data = ''
            form.user_pw2.data = ''
            form.addr1_host_name.data = ''
            form.addr1_port_num.data = 41794
            form.addr2_host_name.data = ''
            form.addr2_port_num.data = 0
    return render_template('cs_entry.html', form=form)

@main.route('/cs_delete/<csid>', methods=['GET', 'POST'])
@login_required
def cs_delete(csid):
    form = FormCsDelete()
    xid = int(current_user.get_id())
    if request.method == 'POST':
        if form.validate_on_submit():
            cs = None
            temp_id = int(form.cs_id.data)
            if temp_id > 0:
                cs = ControlSystem.query.filter_by(id=temp_id, user_id=xid).first()
            if cs is not None:
                db.session.delete(cs)
                db.session.commit()
                delete_project_folders(cs.cs_uuid)
            return redirect('/cs')
    if request.method == 'GET':
        csi = int(csid)
        cs = ControlSystem.query.filter_by(id=csi, user_id=xid).first()
        if cs is not None:
            form.cs_id.data = str(csi)
            form.name.data = cs.cs_name
    return render_template('cs_delete.html', form=form)


@main.route('/upload/<csid>', methods=['GET', 'POST'])
@login_required
def upload_file(csid):
    form = FileUpload()
    xid = int(current_user.get_id())
    csi = int(csid)
    cs = ControlSystem.query.filter_by(id=csi, user_id=xid).first()
    if cs is not None:
        if request.method == 'POST':
            file = form.zip_file.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = os.path.join('/home/colin/uploads', cs.cs_uuid, "upload")
                file.save(os.path.join(upload_folder, filename))
                # TODO: Now the uploaded file needs to be processed
                return redirect(url_for('uploaded_file', filename=filename))
        if request.method == 'GET':
            if cs is not None:
                form.cs_id.data = str(csi)
                form.name.data = cs.cs_name
    return render_template('file_upload.html', form=form)

@main.route('/hhh')
def home_page():
    return render_template_string("""
        {% extends "base.html" %}
        {% block content %}
            <p>{{ url_for('user.logout') }}>
            <p>{{ url_for('user.login') }}>
        {% endblock %}
        """)

# Untility methods are here for now but may be moved to a separate file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ['zip']

def create_project_folders(cs_uuid):
    """
    TODO: Use the config framework for variables in this class
          See: http://stackoverflow.com/a/23037071/953365
    Create the project folder heirarchy: See the notes.txt file for more details
    :param cs_uuid: The uuid of the project which is used as the top-level folder
    :return: None
    """
    root_path = '/home/colin/uploads'
    # Top level folder
    root_project = os.path.join(root_path, cs_uuid)
    if not os.path.exists(root_project):
       os.makedirs(root_project)
    # Now, the sub-folders
    sub_folder = os.path.join(root_project, "upload")
    if not os.path.exists(sub_folder):
        os.makedirs(sub_folder)
    sub_folder = os.path.join(root_project, "unpack")
    if not os.path.exists(sub_folder):
        os.makedirs(sub_folder)
    sub_folder = os.path.join(root_project, "output_files")
    if not os.path.exists(sub_folder):
        os.makedirs(sub_folder)
    sub_folder = os.path.join(root_project, "bb_package")
    if not os.path.exists(sub_folder):
        os.makedirs(sub_folder)

def delete_project_folders(cs_uuid):
    """
    Delete the project folder hierarchy created in the above step. See the notes.txt file for more details
    :param cs_uuid: The uuid of the project which is used as the top-level folder
    :return: None
    """
    root_path = '/home/colin/uploads'
    # Top level folder
    root_project = os.path.join(root_path, cs_uuid)
    if os.path.exists(root_project):
        shutil.rmtree(root_project, True)

