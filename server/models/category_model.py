from server.modules import ma, db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return '<Category - Id: {0}, Category: {1}>' \
            .format(self.id, self.category)


class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category