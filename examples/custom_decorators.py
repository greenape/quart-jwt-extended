from functools import wraps

from quart import Quart, jsonify, request
from quart_jwt_extended import (
    JWTManager,
    verify_jwt_in_request,
    create_access_token,
    get_jwt_claims,
)

app = Quart(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


# Here is a custom decorator that verifies the JWT is present in
# the request, as well as insuring that this user has a role of
# `admin` in the access token
def admin_required(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        await verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims["roles"] != "admin":
            return dict(msg="Admins only!"), 403
        else:
            return await fn(*args, **kwargs)

    return wrapper


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    if identity == "admin":
        return {"roles": "admin"}
    else:
        return {"roles": "peasant"}


@app.route("/login", methods=["POST"])
async def login():
    username = (await request.get_json()).get("username", None)
    access_token = create_access_token(username)
    return dict(access_token=access_token)


@app.route("/protected", methods=["GET"])
@admin_required
async def protected():
    return dict(secret_message="go banana!")


if __name__ == "__main__":
    app.run()
