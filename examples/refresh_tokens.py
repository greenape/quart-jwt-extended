from quart import Quart, jsonify, request
from quart_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    jwt_refresh_token_required,
    create_refresh_token,
    get_jwt_identity,
)

app = Quart(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
async def login():
    username = (await request.get_json()).get("username", None)
    password = (await request.get_json()).get("password", None)
    if username != "test" or password != "test":
        return {"msg": "Bad username or password"}, 401

    # Use create_access_token() and create_refresh_token() to create our
    # access and refresh tokens
    ret = {
        "access_token": create_access_token(identity=username),
        "refresh_token": create_refresh_token(identity=username),
    }
    return ret, 200


# The jwt_refresh_token_required decorator insures a valid refresh
# token is present in the request before calling this endpoint. We
# can use the get_jwt_identity() function to get the identity of
# the refresh token, and use the create_access_token() function again
# to make a new access token for this identity.
@app.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
async def refresh():
    current_user = get_jwt_identity()
    ret = {"access_token": create_access_token(identity=current_user)}
    return ret, 200


@app.route("/protected", methods=["GET"])
@jwt_required
async def protected():
    username = get_jwt_identity()
    return dict(logged_in_as=username), 200


if __name__ == "__main__":
    app.run()
