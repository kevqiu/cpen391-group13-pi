from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(120), unique=True, nullable=False)

    warehouse = db.relationship('Warehouse', backref='item')
    category = db.relationship('Category', backref='item')

class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), unique=True, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    db.relationship('Item', backref='item', lazy=True)

    def __repr__(self):
        return '<Warehouse - Id: {0}, City: {1}, Coordinates: ({2}, {3})>' \
            .format(self.id, self.city, self.latitude, self.longitude)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), unique=True, nullable=False)
    
    db.relationship('Item', backref='item', lazy=True)

    def __repr__(self):
        return '<Category - Id: {0}, Category: {1}>' \
            .format(self.id, self.category)

class ItemSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'warehouse_id', 'category_id', 'timestamp', 'image_path')
        # model = Item

class WarehouseSchema(ma.Schema):
    class Meta:
        fields = ('id', 'city', 'latitude', 'longitude')
        # model = Warehouse

class CategorySchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'category')
        # model = Category

@app.route("/categories")
def categories():
    return jsonify(CategorySchema(many = True).dump(Category.query.all()))

@app.route("/warehouses")
def warehouses():
    return jsonify(WarehouseSchema(many = True).dump(Warehouse.query.all()))

@app.route("/items")
def items():
    return jsonify(ItemSchema(many = True).dump(Item.query.all()))

@app.route("/items/<classtype>")
def items_filtered(classtype):
    return ""
    # classes = [object_as_dict(x) for x in Item.query.filter_by(classification_id=classtype).all()]
    # return json.dumps(classes, indent=4)


if __name__ == "__main__":
    app.run()