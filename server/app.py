from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from sqlalchemy import desc
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []
    # Query all bakeries from the database
    for bakery in Bakery.query.all():
        # Convert each bakery to a dictionary
        bakery_dict = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': str(bakery.created_at),
            'updated_at': str(bakery.updated_at)
        }
        bakeries.append(bakery_dict)

    # Return the list of bakeries as JSON
    response = make_response(jsonify(bakeries), 200)
    response.headers["Content-type"] = "application/json"

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    # Query the bakery by id from the database
    bakery = Bakery.query.get(id)

    if bakery:
        # Convert the bakery and its baked goods to a dictionary
        bakery_data = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': str(bakery.created_at),
            'updated_at': str(bakery.updated_at),
            'baked_goods': [
                {
                    'id': baked_good.id,
                    'name': baked_good.name,
                    'price': baked_good.price,
                    'created_at': str(baked_good.created_at),
                    'updated_at': str(baked_good.updated_at)
                }
                for baked_good in bakery.baked_goods
            ]
        }

        # Return the bakery data as JSON
        return jsonify(bakery_data)
    else:
        # Return a 404 response if the bakery is not found
        return make_response(jsonify({'error': 'Bakery not found'}), 404)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # Query all baked goods, sorted by price in descending order
    baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()

    # Convert the list of baked goods to a list of dictionaries
    baked_goods_list = [
        {
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price,
            'created_at': str(baked_good.created_at),
            'updated_at': str(baked_good.updated_at)
        }
        for baked_good in baked_goods
    ]

    # Return the list of baked goods as JSON
    return jsonify(baked_goods_list)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # Query the most expensive baked good, ordered by price in descending order, and limit to 1 result
    most_expensive_baked_good = BakedGood.query.order_by(desc(BakedGood.price)).first()

    if most_expensive_baked_good:
        # Convert the most expensive baked good to a dictionary
        baked_good_data = {
            'id': most_expensive_baked_good.id,
            'name': most_expensive_baked_good.name,
            'price': most_expensive_baked_good.price,
            'created_at': str(most_expensive_baked_good.created_at),
            'updated_at': str(most_expensive_baked_good.updated_at)
        }

        # Return the most expensive baked good data as JSON
        return jsonify(baked_good_data)
    else:
        # Return a 404 response if no baked goods are found
        return make_response(jsonify({'error': 'No baked goods found'}), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
