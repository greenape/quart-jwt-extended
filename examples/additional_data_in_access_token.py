from quart import Quart, jsonify, request
from quart_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_claims,
)

app = Quart(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


# Using the user_claims_loader, we can specify a method that will be
# called when creating access tokens, and add these claims to the said
# token. This method is passed the identity of who the token is being
# created for, and must return data that is json serializable
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {"hello": identity, "foo": ["bar", "baz"]}


@app.route("/login", methods=["POST"])
async def login():
    username = (await request.get_json()).get("username", None)
    password = (await request.get_json()).get("password", None)
    if username != "test" or password != "test":
        return {"msg": "Bad username or password"}, 401

    ret = {"access_token": create_access_token(username)}
    return ret, 200


# In a protected view, get the claims you added to the jwt with the
# get_jwt_claims() method
@app.route("/protected", methods=["GET"])
@jwt_required
async def protected():
    claims = get_jwt_claims()
    return {"hello_is": claims["hello"], "foo_is": claims["foo"]}, 200


if __name__ == "__main__":
    app.run()
