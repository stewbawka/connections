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
def test_mutual_friends_error(db, testapp, id):
    res = testapp.get('/connections/'+id)   
    assert res.status_code == HTTPStatus.NOT_FOUND

def test_mutual_friends(db, testapp):
    instance = PersonFactory()
    target = PersonFactory()
    mutual_friends = PersonFactory.create_batch(3)
    decoy_friends = PersonFactory.create_batch(5)
    decoy = PersonFactory()
    # SQL error can not add/update child row foriegn key constarin
    db.session.commit()
    # some decoy connections (not mutual)
    for d in decoy_friends:
        ConnectionFactory(from_person_id=d.id, to_person_id=instance.id)
        ConnectionFactory(from_person_id=d.id, to_person_id=target.id)

    for f in mutual_friends:
        ConnectionFactory(from_person_id=instance.id, to_person_id=f.id, connection_type='friend')
        ConnectionFactory(from_person_id=target.id, to_person_id=f.id, connection_type='friend')

    # mutual connections, but not friends
    ConnectionFactory(from_person_id=instance.id, to_person_id=decoy.id, connection_type='coworker')
    ConnectionFactory(from_person_id=target.id, to_person_id=decoy.id, connection_type='coworker')

    db.session.commit()

    expected_mutual_friend_ids = [f.id for f in mutual_friends]

    s = '/people/'+str(instance.id)+'/mutual_friends?target_id='+str(target.id)
    # same call with swap person id and target id 
    s1 = '/people/'+str(target.id)+'/mutual_friends?target_id='+str(instance.id)
    results = testapp.patch(s)
    results1 = testapp.patch(s1)

    assert len(results) == 3
    assert len(results1) == 3
    for f in results:
        assert f in expected_mutual_friend_ids
    for f in results1:
        assert f in expected_mutual_friend_ids
    for person in results.json:
         for field in EXPECTED_FIELDS:
             assert field in person
