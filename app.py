"""Flask app for adopt app."""
import os
import requests

from flask import Flask, render_template, redirect, flash

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]

connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


@app.get("/")
def show_pets():
    """List pets with name, photo, and avalibility."""

    pet_list = get_pets()

    pets = Pet.query.all()

    return render_template("pets.html", pets=pets)


@app.route("/add", methods=["GET", "POST"])
def handle_pet_form():
    """Show pet addition form and handle new pet submission"""

    form = AddPetForm()

    if form.validate_on_submit():

        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)

        db.session.add(pet)
        db.session.commit()

        flash(f"{pet.name} added!")
        return redirect("/")

    else:
        return render_template("add_pet_form.html", form=form)


@app.get("/<int:pet_id>")
def display_pet_details(pet_id):
    """Display pet details."""

    pet = Pet.query.get(pet_id)

    return render_template("pet_detail_page.html", pet=pet)



@app.route("/<int:pet_id>/edit", methods=["GET", "POST"])
def handle_pet_edit_form(pet_id):
    """Show pet editing form and handle pet info edits"""

    pet = Pet.query.get(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():

        photo_url = form.photo_url.data
        notes = form.notes.data
        available = form.available.data

        pet.photo_url = photo_url
        pet.notes = notes
        pet.available = available

        db.session.add(pet)
        db.session.commit()

        flash(f"{pet.name} updated!")
        return redirect(f"/{pet_id}")

    else:
        return render_template("edit_pet_form.html", form=form, pet=pet)



def get_pets():
    """Get pets from petfinder API"""

    token = get_pet_token()


def get_pet_token():
    """Get petfinder token"""

    response = requests.get(f"https://api.petfinder.com/v2/oauth2/token?\
        grant_type=client_credentials&client_id={API_KEY}&client_secret={API_SECRET}")
    breakpoint()

    token = response["access_token"]

    return token