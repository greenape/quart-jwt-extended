from quart import Quart, jsonify, request
from quart_jwt_extended import (
    JWTManager,
    jwt_optional,
    create_access_token,
    get_jwt_identity,
)

app = Quart(__name__)

# Setup the Quart-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
async def login():
    username = (await request.get_json()).get("username", None)
    password = (await request.get_json()).get("password", None)
    if not username:
        return {"msg": "Missing username parameter"}, 400
    if not password:
        return {"msg": "Missing password parameter"}, 400

    if username != "test" or password != "test":
        return {"msg": "Bad username or password"}, 401

    access_token = create_access_token(identity=username)
    return dict(access_token=access_token), 200


@app.route("/partially-protected", methods=["GET"])
@jwt_optional
async def partially_protected():
    # If no JWT is sent in with the request, get_jwt_identity()
    # will return None
    current_user = get_jwt_identity()
    if current_user:
        return dict(logged_in_as=current_user), 200
    else:
        return dict(logged_in_as="anonymous user"), 200


if __name__ == "__main__":
    app.run()
