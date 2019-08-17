import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
        jwt_required,
        get_jwt_claims,
        jwt_optional,
        get_jwt_identity,
        fresh_jwt_required
)
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank'
    )

    parser.add_argument('store_id',
        type=float,
        required=True,
        help='Store ID must be there'
    )


    @jwt_required  # no brackets due to jwt_required extended from flask_jwt_extended
    def get(self,name):
        item =ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'item not found'},404

    @fresh_jwt_required
    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item with name {} already exists'.format(name)}, 400

        request_data = Item.parser.parse_args()
        item = ItemModel(name,request_data['price'],request_data['store_id']) # silent = True --> Does not give an error , returns none
        try:
            item.save_to_db()
        except:
            return {'message':'An error occured while inserting'}, 500  #Internal server error

        return item.json(), 201

    @jwt_required
    def delete(self,name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message':'Admin priviledge required'}

        item=ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message':'item deleted'}

    def put(self,name):
        request_data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, request_data['price'],request_data['store_id']) # else **data
        else:
            item.price = request_data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items':items}
        return {'items': [item['name'] for item in items],
                'message':'More info available if you login'
        }
