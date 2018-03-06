# from ..server import db

# class Warehouse(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     city = db.Column(db.String(50), nullable=False)
#     latitude = db.Column(db.F, nullable=False)
#     longitude = db.Column(db.String(50), nullable=False)
#     items = db.relationship('Item', backref='item', lazy=True)