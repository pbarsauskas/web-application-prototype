from flask_wtf import Form
from wtforms import StringField, PasswordField, DecimalField,  SelectField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)
from models import Users

def name_exists(form, field):
    if Users.select().where(Users.username == field.data).exists():
        raise ValidationError('User with that name already exists')
    
def email_exists(form, field):
    if Users.select().where(Users.email == field.data).exists():
        raise ValidationError('User with that email already exists')


class RegisterForm(Form):
    
    title = SelectField(
                        label= u'Title',
                        choices=[('',''),('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Miss', 'Miss'),('Ms','Ms')],
                        option_widget=None,
                        validators=[
                                    DataRequired(),
                                    Regexp(r'^[a-zA-Z]+$',
                                           message=("Title has to be selected")
                                           )
                                    ],
                        description='Title'
                        )
    
    first_name = StringField(
                        'First name',
                        validators=[
                                    DataRequired(),
                                    Regexp(r'^[a-zA-Z]+$',
                                           message=("Letters only")
                                           )
                                    ]
                        )
    
    middle_name = StringField(
                        'Middle name'
                        )
    
    last_name = StringField(
                        'Last name',
                        validators=[
                                    DataRequired(),
                                    Regexp(r'^[a-zA-Z]+$',
                                           message=("Letters only")
                                           )
                                    ]
                        )
    
    phone_number= StringField(
                        'Phone number',
                        validators=[
                                    DataRequired(),
                                    Regexp(r'^-?[0-9]+$' ,
                                           message=("Telephone mumer - Numbers 0 to 9 only"))
                                    ]
                        )
    
    username =  StringField(
                            'Username',
                            validators=[
                                        DataRequired(),
                                        Regexp(
                                             r'^[a-zA-Z0-9_]+$',
                                             message=("Username should be one word, letter, "
                                             "number, and underscores only.")
                                               ),
                                        name_exists
                                        ]
                            
                            )
    email = StringField(
                        'Email',
                        validators=[
                                    DataRequired(),
                                    Email(),
                                    email_exists
                                    ]
                        )
    password = PasswordField(
                             'Password',
                             validators=[
                                         DataRequired(),
                                         Length(min=2),
                                         EqualTo('password2', message ='Passwords must match')
                                         
                                         ]
                             )
    password2 = PasswordField(
                              'Confirm Password',
                              validators=[DataRequired()]
                              )
    
class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class DataEntry(Form):
    input1 =  DecimalField('Enter numeric value',
                           validators=[DataRequired()]
                           )
