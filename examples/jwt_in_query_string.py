from quart import Quart, jsonify, request

from quart_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
)

# IMPORTANT NOTE:
# In most cases this is not recommended! It can lead some some
# security issues, such as:
#    - The browser saving GET request urls in it's history that
#      has a JWT in the query string
#    - The backend server logging JWTs that are in the url
#
# If possible, you should use headers instead!

app = Quart(__name__)
app.config["JWT_TOKEN_LOCATION"] = ["query_string"]
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


# The default query paramater where the JWT is looked for is `jwt`,
# and can be changed with the JWT_QUERY_STRING_NAME option. Making
# a request to this endpoint would look like:
# /protected?jwt=<ACCESS_TOKEN>
@app.route("/protected", methods=["GET"])
@jwt_required
async def protected():
    return dict(foo="bar")


if __name__ == "__main__":
    app.run()
