from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'barkmeow123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

###########################################################################################

@app.route('/')
def pets_list():

    """List all pets"""

    pets = Pet.query.all()
    return render_template('pet_list.html', pets=pets)

@app.route('/pets/add', methods=['GET', 'POST'])
def add_pet():
    """Add a pet"""

    form = AddPetForm()
    
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_pet = Pet(**data)
        db.session.add(new_pet)
        db.session.commit() 
        flash(f"{new_pet.name} added")
        return redirect('/')

    else:
        return render_template('add_pet_form.html', form=form)

@app.route('/pets/<int:pet_id>/edit', methods=['GET', 'POST'])
def edit_pet(pet_id):
    """Edit a pet"""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.add(pet)
        db.session.commit()
        flash(f"{pet.name} has been updated")
        return redirect('/')

    else:
        return render_template('edit_pet_form.html', form=form)






        




