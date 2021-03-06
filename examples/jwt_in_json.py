from quart import Quart, jsonify, request

from quart_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
)

app = Quart(__name__)

# IMPORTANT: Body is meaningless in GET requests, so using json
# as the only lookup method means that the GET method will become
# unauthorized in any protected route, as there's no body to look for.

app.config["JWT_TOKEN_LOCATION"] = ["json"]
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!

jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
async def login():
    username = (await request.get_json()).get("username", None)
    password = (await request.get_json()).get("password", None)
    if username != "test" or password != "test":
        return {"msg": "Bad username or password"}, 401

    access_token = create_access_token(identity=username)
    return dict(access_token=access_token)


# The default attribute name where the JWT is looked for is `access_token`,
# and can be changed with the JWT_JSON_KEY option.
# Notice how the route is unreachable with GET requests.
@app.route("/protected", methods=["GET", "POST"])
@jwt_required
async def protected():
    return dict(foo="bar")


if __name__ == "__main__":
    app.run()
