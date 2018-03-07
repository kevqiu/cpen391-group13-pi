from server.extensions import ma, db


class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), unique=True, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Warehouse - Id: {0}, City: {1}, Coordinates: ({2}, {3})>' \
            .format(self.id, self.city, self.latitude, self.longitude)


class WarehouseSchema(ma.ModelSchema):
    class Meta:
        model = Warehouse