from server.extensions import ma, db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(120), unique=True, nullable=False)


class ItemSchema(ma.ModelSchema):
    class Meta:
        model = Item
        include_fk = True
