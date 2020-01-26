from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", required=True, type=str)
    parser.add_argument("password", required=True, type=str)

    def post(self):
        request_data = self.parser.parse_args()
        user = UserModel.find_by_username(request_data["username"])
        if user:
            return {"message": f"User {request_data['username']} already exists!"}, 400
        else:
            UserModel(**request_data).save_user_to_db()
            return {"message": "User has been created successfully"}, 201


