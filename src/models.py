import datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from peewee import *

DATABASE = SqliteDatabase('database.db')

class Users(UserMixin, Model):
    username =  CharField(unique=True)
    email = CharField(unique=True)
    title = CharField(max_length=4)
    first_name = CharField()
    middle_name = CharField()
    last_name = CharField()
    phone_number = IntegerField()
    password = CharField(max_length=100)
    date_created = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default= False)
    
    class Meta:
        database = DATABASE
        order_by = ('-date_created',)
        
    @classmethod
    def create_user(cls, username, email, title, first_name, middle_name, last_name, phone_number, password, admin=False):
        try:
            cls.create(
                username=username,
                email=email,
                title=title,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                phone_number=phone_number,
                password=generate_password_hash(password),
                is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")
        
    @classmethod
    def delete_user(cls, username):
        try:
            cls.delete(username=username)
        except IntegrityError:
            raise ValueError("User already exists")


class DataEntry(Model):
    input1 = DecimalField()
    
    class Meta:
        database = DATABASE

    @classmethod
    def create_entry(cls, input1):
        try:
            cls.create(
                input1=input1
               )
        except IntegrityError:
            raise ValueError("Please, enter numeric value")

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Users], safe=True)
    DATABASE.create_tables([DataEntry], safe=True)
    DATABASE.close()
