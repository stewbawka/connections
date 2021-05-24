from http import HTTPStatus

import pytest
from sqlalchemy.sql.elements import Null
from tests.factories import ConnectionFactory, PersonFactory

EXPECTED_FIELDS = [
    'id',
    'first_name',
    'last_name',
    'email',
]


@pytest.mark.parametrize('id', [
    pytest.param(''),
    pytest.param('abc')
])
def test_can_get_connections_error(db, testapp, id):
    res = testapp.get('/connections/'+id)   
    assert res.status_code == HTTPStatus.NOT_FOUND

def test_can_get_connections(db, testapp):
    instance = PersonFactory()
    decoy_friends = PersonFactory.create_batch(10)
    db.session.commit()
    for d in decoy_friends:
        ConnectionFactory(from_person_id=instance.id, to_person_id=d.id)
        
    db.session.commit()
    s = '/connections/'+str(instance.id)
    res = testapp.get(s)

    assert res.status_code == HTTPStatus.OK

    assert len(res.json) == 10
    for person in res.json:
         for field in EXPECTED_FIELDS:
             assert field in person
