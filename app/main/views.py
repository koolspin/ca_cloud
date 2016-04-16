import uuid
from flask import render_template, render_template_string, request, redirect
from flask.ext.login import current_user
from flask_user import login_required
from . import main
from .forms import FormControlSystem, FormCsDelete
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
            return redirect('/cs')
    if request.method == 'GET':
        csi = int(csid)
        cs = ControlSystem.query.filter_by(id=csi, user_id=xid).first()
        if cs is not None:
            form.cs_id.data = str(csi)
            form.name.data = cs.cs_name
    return render_template('cs_delete.html', form=form)

@main.route('/hhh')
def home_page():
    return render_template_string("""
        {% extends "base.html" %}
        {% block content %}
            <p>{{ url_for('user.logout') }}>
            <p>{{ url_for('user.login') }}>
        {% endblock %}
        """)

