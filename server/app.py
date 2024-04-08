from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder = jsonify

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(jsonify(bakeries), 200)

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if not bakery:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)

    if request.method == 'GET':
        bakery_serialized = bakery.to_dict()
        response = make_response(jsonify(bakery_serialized), 200)
        return response
    elif request.method == 'PATCH':
        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))

        db.session.add(bakery)
        db.session.commit()

        bakery_dict = bakery.to_dict()

        response = make_response(jsonify(bakery_dict), 200)
        return response

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.json
    baked_good = BakedGood(name=data['name'], price=data['price'], bakery_id=data['bakery_id'])
    db.session.add(baked_good)
    db.session.commit()
    return make_response(jsonify(baked_good.to_dict()), 201)

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    if not baked_good:
        return make_response(jsonify({'error': 'Baked Good not found'}), 404)

    db.session.delete(baked_good)
    db.session.commit()

    response_body = {
        "delete_successful": True,
        "message": "Baked Good deleted."
    }
    response = make_response(jsonify(response_body), 200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
