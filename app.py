from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "eifjawloijcvliejfiwnbnsliex0"

connect_db(app)


@app.route('/', methods=['GET'])
def home_route():
    """ Render simple interface for listing cupcakes from cupcakes_db,
    and show a form that allows user to add a new cupcake """

    cupcakes = Cupcake.query.all()
    return render_template('front.html', cupcakes=cupcakes)


@app.route('/api/cupcakes')
def list_cupcakes():
    """ Returns list of cupcakes from cupcakes_db in JSON """
    list_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=list_cupcakes)


@app.route('/api/cupcakes', methods=['POST'])
def post_cupcake():
    """ Input JSON to submit a new cupcake to cupcakes_db """
    new_cupcake = Cupcake(
        flavor=request.json['flavor'],
        size=request.json['size'],
        rating=request.json['rating'],
        image=request.json.get('image', None)
    )
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return(response_json, 201)


@app.route('/api/cupcakes/<int:cupcake_id>')
def cupcake_detail(cupcake_id):
    """ Returns details about a single cupcake from cupcakes_db in JSON """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """ Update a cucpake from cupcakes_db by inputting JSON """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """ Delete a cupcake from cupcakes_db """
    cupcake = Cupcake.query.get(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted cupcake")
