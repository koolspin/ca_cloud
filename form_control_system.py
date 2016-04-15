from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, BooleanField, PasswordField, SubmitField
from wtforms.validators import Required

class FormControlSystem(Form):
    name = StringField('System Name', validators=[Required()])
    ipid = StringField('IPID', validators=[Required()])
    ssl_on = BooleanField('SSL')
    user_id = StringField('User ID')
    user_pw = PasswordField('User PW')
    addr1_host_name = StringField('Addr1 Host Name', validators=[Required()])
    addr1_port_num = IntegerField('Addr1 CIP Port', validators=[Required()])
    addr2_host_name = StringField('Addr2 Host Name')
    addr2_port_num = IntegerField('Addr2 CIP Port')
    submit = SubmitField('Submit')

