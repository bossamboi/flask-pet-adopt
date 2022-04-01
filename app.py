"""Flask app for adopt app."""

from flask import Flask, render_template, redirect, flash

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


@app.get("/")
def show_pets():
    """List pets with name, photo, and avalibility"""

    pets = Pet.query.all()

    return render_template("pets.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def handle_pet_form():
    """Show pet addition form and handle new pet submission"""

    form = AddPetForm()
    # form = AddPetForm(obj=pet)

    if form.validate_on_submit():
        # process form and redirect somewhere
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(pet)
        db.session.commit()

        flash(f"{name} added!")
        return redirect("/")

    else:
        return render_template("add_pet_form.html", form=form)



@app.route("/<int:pet_id>/edit", methods=["GET", "POST"])
def handle_pet_edit_form(pet_id):
    """Show pet editing form and handle pet info edits"""

    pet = Pet.query.get(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        # process form and redirect somewhere

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