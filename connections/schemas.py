from marshmallow import fields, validates, ValidationError
from marshmallow_enum import EnumField

from connections.extensions import ma
from connections.models.connection import Connection, ConnectionType
from connections.models.person import Person
import re 
from datetime import date

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

class BaseModelSchema(ma.ModelSchema):
    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)


class PersonSchema(BaseModelSchema):

    class Meta:
        model = Person
    
    # email validation
    @validates('email') 
    def validate_Email(self, email):
        if not re.match(regex, email):
            raise ValidationError('Not a valid email address.') 
        return email

    # DOB validation
    @validates('date_of_birth') 
    def validate_Dob(self, date_of_birth):
        if (date_of_birth > date.today()):
            raise ValidationError('Cannot be in the future.') 
        return date_of_birth    

class ConnectionSchema(BaseModelSchema):
    from_person_id = fields.Integer()
    to_person_id = fields.Integer()
    connection_type = EnumField(ConnectionType)

    class Meta:
        model = Connection

