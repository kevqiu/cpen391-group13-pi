from server.modules import ma, db


class Cycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Cycle - Id: {0}, Start: {1}, End: {2})>' \
            .format(self.id, self.start_time, self.end_time)


class CycleSchema(ma.ModelSchema):
    class Meta:
        model = Cycle