from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.get_store_by_name(name)
        if store:
            return store.json()
        else:
            return {"Message": f"Store with name '{name}' is not found"}, 404

    def post(self, name):
        if StoreModel.get_store_by_name(name):
            return {"Message": f"Store with name '{name}' already exists"}, 400
        else:
            store = StoreModel(name)
            store.save_store_to_db()
            return store.json(), 201

    def delete(self, name):
        store = StoreModel.get_store_by_name(name)
        if store:
            store.delete_store()
            return {"Message": f"Store '{name}' has been deleted"}
        else:
            return {"Message": f"Store with name '{name}' is not found"}, 404


class StoresList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
