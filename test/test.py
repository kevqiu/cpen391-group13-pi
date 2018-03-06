from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import sys, json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    classification_id = db.Column(db.Integer, db.ForeignKey('classification.id'), nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(120), unique=True, nullable=False)

    warehouse = db.relationship('Warehouse', backref=db.backref('item', lazy=True))
    classification = db.relationship('Classification', backref=db.backref('item', lazy=True))

    # @property
    # def warehouse(self):
    #     return self._warehouse.warehouse

    # @property
    # def classification(self):
    #     return self._classification.classification

class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), unique=True, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    #items = db.relationship('Item', backref='item', lazy=True)

class Classification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classification = db.Column(db.String(50), unique=True, nullable=False)
    #items = db.relationship('Item', backref='item', lazy=True)

    # def __repr__(self):
    #     return '<Classification %r>' % self.classification

@app.route("/classifications")
def classifications():
    classes = [object_as_dict(x) for x in Classification.query.all()]
    return json.dumps(classes, indent=4)

@app.route("/warehouses")
def warehouses():
    classes = [object_as_dict(x) for x in Warehouse.query.all()]
    return json.dumps(classes, indent=4)

@app.route("/items")
def items():
    classes = [object_as_dict(x) for x in Item.query.all()]
    return json.dumps(classes, indent=4)

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

if __name__ == "__main__":
    app.run()