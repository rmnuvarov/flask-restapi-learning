from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", required=True, type=float)
    parser.add_argument("store_id", required=True, type=int,
                        help="Every item must have store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
            return item.json()
        else:
            return {"Message": f"Item with name {name} is not found"}, 404

    def post(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
            return {"Message": f"Item with name {name} already exists!"}, 400
        else:
            request_data = self.parser.parse_args()
            item_to_create = ItemModel(name=name, price=request_data["price"], store_id=request_data["store_id"])
            item_to_create.save_item_to_db()
            return item_to_create.json(), 201

    def put(self, name):
        request_data = self.parser.parse_args()
        item = ItemModel.get_item_by_name(name)
        if item:
            item.price = request_data["price"]
        else:
            item = ItemModel(name, price=request_data["price"], store_id=request_data["store_id"])

        item.save_item_to_db()
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.get_item_by_name(name)
        if not item:
            return {"Error": f"item with name '{name}' doesnt exits!"}, 404
        else:
            item.delete_item()
            return {name: "DELETED"}, 200


class ItemsList(Resource):
    def get(self):
        items = ItemModel.get_items_jsons()
        return {"items": items}, 200

