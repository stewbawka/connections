from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model


class Person(Model, CRUDMixin, CreatedUpdatedMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(145), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    connections = db.relationship('Connection', backref='Person', lazy=True, foreign_keys='Connection.from_person_id')

    def mutual_friends(self, person):
        # Query to find mutual friend in ORM with join and filter with type friend
        list1_as_set = set([f.to_person_id for f in self.connections])
        return list1_as_set.intersection([f.to_person_id for f in person.connections]) 
        #return db.session.query(self.connections).add_columns(self.connections.to_person_id).join(person.connections).filter(person.connections.to_person_id == self.connections.to_person_id ).all()
