"""Models for adopt app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)


class Pet(db.Model):
    """Creates pet"""

    __tablename__ = "pets"

    def __repr__(self):
        """Show info about pet."""

        p = self
        return f"<Pet ID{p.id}, {p.name} is a {p.age} {p.species}.\
            Photo is {p.photo_url} and the availibilty is {p.available}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                    nullable=False)
    species = db.Column(db.Text,
                    nullable=False)
    photo_url = db.Column(db.Text,
                    nullable=False,
                    default="")
    age = db.Column(db.Text,
                    nullable=False)
    notes = db.Column(db.Text,
                    nullable=True)
    available = db.Column(db.Boolean,
                    nullable=False,
                    default=True)


