import os, sys
#, config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

#from .controllers.data_controller import data
#from .controllers.control_controller import control

app = Flask(__name__)

# db_path = os.path.dirname(sys.modules['__main__'].__file__) + config.db_path
app.config['SQLALCHEMY_DATABASE_URI'] =  "..\\db\\test.db"
db = SQLAlchemy(app)

#app.register_blueprint(data)
#app.register_blueprint(control)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    classification_id = db.Column(db.Integer, db.ForeignKey('classification.id'), nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    classification = db.Column(db.String(120), nullable=False)
    image_path = db.Column(db.String(120), nullable=False)

@app.route("/")
def test():
    print(Item.query.all(), file=sys.stderr)