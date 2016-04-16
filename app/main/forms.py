from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, BooleanField, PasswordField, SubmitField, HiddenField
from wtforms.validators import Required, NumberRange

class FormControlSystem(Form):
    cs_id = HiddenField()
    name = StringField('System Name', validators=[Required()])
    ipid = StringField('IPID', validators=[Required()])
    ssl_on = BooleanField('SSL')
    user_id = StringField('User ID')
    user_pw = PasswordField('User PW')
    user_pw2 = PasswordField('Confirm PW')
    addr1_host_name = StringField('Addr1 Host Name', validators=[Required()])
    addr1_port_num = IntegerField('Addr1 CIP Port', validators=[Required(), NumberRange(min=1, max=65536)])
    addr2_host_name = StringField('Addr2 Host Name')
    addr2_port_num = IntegerField('Addr2 CIP Port', validators=[NumberRange(min=0, max=65536)])
    submit = SubmitField('Submit')

class FormCsDelete(Form):
    cs_id = HiddenField()
    name = StringField('System Name')
    submit = SubmitField('Delete')
