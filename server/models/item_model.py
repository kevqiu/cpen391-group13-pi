from server.modules import ma, db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Item - Id: {0}, WarehouseId: {1}, CategoryId: {2}>, DateTime: {3}'\
            .format(self.id, self.warehouse_id, self.category_id, self.datetime)

class ItemSchema(ma.ModelSchema):
    class Meta:
        model = Item
        include_fk = True
