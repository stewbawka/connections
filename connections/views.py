from http import HTTPStatus

from flask import Blueprint, request
from webargs import fields
from webargs.flaskparser import use_args

from connections.models.person import Person
from connections.models.connection import Connection, ConnectionType
from connections.schemas import ConnectionSchema, PersonSchema

from sqlalchemy import join

blueprint = Blueprint('connections', __name__)


@blueprint.route('/people', methods=['GET'])
def get_people():
    people_schema = PersonSchema(many=True)
    people = Person.query.all()
    return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people', methods=['POST'])
@use_args(PersonSchema(), locations=('json',))
def create_person(person):
    person.save()
    return PersonSchema().jsonify(person), HTTPStatus.CREATED


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    connection.save()
    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED

# get services '/connections/{from})
@blueprint.route('/connections/<int:fromid>', methods=['GET'])
def get_connections(fromid):
    people_schema = PersonSchema(many=True)
    person = Person.query.join(Connection ,Connection.to_person_id == Person.id).filter(Connection.from_person_id == fromid).all()
    return people_schema.jsonify(person), HTTPStatus.OK

# patch services '/connections?fromid=instance.id&toid=target.id&type='coworker')
@blueprint.route('/connections', methods=['PATCH'])
#@use_args(ConnectionSchema(), locations=('json',)) NOT BEST SOLUTION
def patch_connections():
    connection = ConnectionSchema()
    connection.from_person_id= request.args.get('fromid')
    connection.to_person_id=request.args.get('toid')
    connection.connection_type=ConnectionType(request.args.get('type'))
    connection_1 = Connection.query.filter(Connection.from_person_id==connection.from_person_id).filter(Connection.to_person_id==connection.to_person_id)
    connection_2 = Connection.query.filter(Connection.to_person_id==connection.from_person_id).filter(Connection.from_person_id==connection.to_person_id)
    connection_2.connection_type = connection.connection_type
    connection_1.connection_type = connection.connection_type
    connection_1.update({"connection_type" : connection.connection_type})
    connection_2.update({"connection_type" : connection.connection_type})
    return ConnectionSchema().jsonify(connection_1), HTTPStatus.OK 
