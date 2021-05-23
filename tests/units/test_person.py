import pytest
from tests.factories import ConnectionFactory, PersonFactory

def test_mutual_friends(db):
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

    results = instance.mutual_friends(target)

    assert len(results) == 3
    for f in results:
