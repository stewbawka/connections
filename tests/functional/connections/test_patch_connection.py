from http import HTTPStatus

import pytest
from sqlalchemy.sql.elements import Null
from tests.factories import ConnectionFactory, PersonFactory
import json

@pytest.mark.parametrize('fromid, toid, type', [
    pytest.param('','',''),
    pytest.param('abc','abc','abc'),
    pytest.param(Null,Null,Null)
])
def test_can_patch_connections_error(db, testapp, fromid, toid, type):
    s = '/connections?fromid='+str(fromid)+'&toid='+str(toid)+'&type='+str(type)
    res = testapp.patch(s)
    print(res)
    assert res.status_code == HTTPStatus.BAD_REQUEST

def test_can_patch_connections_wrongtype(db, testapp):
    instance = PersonFactory()
    target = PersonFactory()
    db.session.commit()
    connection_1 = ConnectionFactory(from_person_id=instance.id, to_person_id=target.id)  
    connection_2 = ConnectionFactory(from_person_id=target.id, to_person_id=instance.id)
    db.session.commit()
    s = '/connections?fromid='+str(instance.id)+'&toid='+str(target.id)+'&type='+str('abc')
    res = testapp.patch(s)
    assert res.status_code == HTTPStatus.BAD_REQUEST

def test_can_patch_connections(db, testapp):
    instance = PersonFactory()
    target = PersonFactory()
    db.session.commit()
    connection_1 = ConnectionFactory(from_person_id=instance.id, to_person_id=target.id)  
    connection_2 = ConnectionFactory(from_person_id=target.id, to_person_id=instance.id)
    db.session.commit()
    s = '/connections?fromid='+str(instance.id)+'&toid='+str(target.id)+'&type='+str('coworker')
    res = testapp.patch(s)
    assert res.status_code == HTTPStatus.OK
    assert res.json['connection_type'] == "coworker"
