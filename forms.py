"""Forms for adopt app."""
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, URLField, BooleanField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Optional, URL, Length

class AddPetForm(FlaskForm):
    """Form for adding pets."""

    name = StringField("Pet Name",
                        validators=[InputRequired()])

    species = SelectField("Species",
        choices=[('cat', 'Cat'),
                ('dog', 'Dog'),
                ('porcupine', 'Porcupine')])

    photo_url = URLField("Photo URL",
                        validators=[Optional(), URL()])

    age = SelectField("Age",
        choices=[('baby', 'Baby'),
                ('young', 'Young'),
                ('adult', 'Adult'),
                ('senior', "Senior")])

    notes = TextAreaField("Notes",
                        validators=[Optional(), Length(min=10)])


class EditPetForm(FlaskForm):
    """Form for editing pets."""

    photo_url = URLField("Photo URL",
                        validators=[Optional(), URL()])

    notes = TextAreaField("Notes",
                        validators=[Optional(), Length(min=10)])

    available = BooleanField("Available?")
