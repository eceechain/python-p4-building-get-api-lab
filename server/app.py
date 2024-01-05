from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from sqlalchemy import desc
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []

    for bakery in Bakery.query.all():
        bakery_dict = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': str(bakery.created_at),
            'updated_at': str(bakery.updated_at)
        }
        bakeries.append(bakery_dict)

    response = make_response(
        jsonify(bakeries),
        200
    )
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)

    if bakery:
        bakery_dict = bakery.to_dict()
        response = make_response(
            jsonify(bakery_dict),
            200
        )
    else:
        response = make_response(
            jsonify({'error': 'Bakery not found'}),
            404
        )

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()

    baked_goods_list = [baked_good.to_dict() for baked_good in baked_goods]

    response = make_response(
        jsonify(baked_goods_list),
        200
    )

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_baked_good = BakedGood.query.order_by(desc(BakedGood.price)).first()

    if most_expensive_baked_good:
        most_expensive_baked_good_dict = most_expensive_baked_good.to_dict()
        response = make_response(
            jsonify(most_expensive_baked_good_dict),
            200
        )
    else:
        response = make_response(
            jsonify({'error': 'No baked goods found'}),
            404
        )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
