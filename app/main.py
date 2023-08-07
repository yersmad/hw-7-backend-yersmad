from fastapi import Cookie, FastAPI, Form, Request, Response, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from .flowers_repository import Flower, FlowersRepository
from .purchases_repository import Purchase, PurchasesRepository
from .users_repository import User, UsersRepository

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


flowers_repository = FlowersRepository()
purchases_repository = PurchasesRepository()
users_repository = UsersRepository()


def encode_jwt(username: str):
    body = {"username": username}
    token = jwt.encode(body, "test", 'HS256')
    dict_token = {"token": token}
    return dict_token["token"]


def decode_jwt(token: str):
    data = jwt.decode(token, "test", 'HS256')
    return data["username"]


@app.post("/signup")
def post_signup(
    username: str=Form(),
    full_name: str=Form(),
    password: str=Form()
):
    user = User(username=username, full_name=full_name, password=password)
    if users_repository.get_user_by_username(username=username) != None:
        return Response(
            content=b"Email is already exists\n",
            media_type="text/plain",
            status_code=403
        )

    users_repository.save_user(user=user)
    return Response(status_code=200)


@app.post("/login")
def post_login(
    username: str=Form(),
    password: str=Form()
):
    user = users_repository.get_user_by_username(username=username)
    if not user:
        return Response(
            content=b"User not found\n",
            media_type="text/plain",
            status_code=404
        )

    if user.password != password:
        return Response(
            content=b"Incorrect password\n",
            media_type="text/plain",
            status_code=401
        )

    token = encode_jwt(username=username)
    return {
        "access token": token,
        "type": "bearer"
    }


@app.get("/profile")
def get_profile(token: str=Depends(oauth2_scheme)):
    user_name = decode_jwt(token=token)
    user = users_repository.get_user_by_username(username=user_name)

    if not user:
        return Response(
            content=b"User not found\n",
            media_type="text/plain",
            status_code=404
        )

    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name
    }


@app.get("/flowers")
def get_flowers(token: str=Depends(oauth2_scheme)):
    flowers = flowers_repository.get_all()
    return {"flowers": flowers}


@app.post("/flowers")
def post_flowers(
    name: str=Form(),
    count: int=Form(),
    cost: int=Form(),
    token: str=Depends(oauth2_scheme)
):
    flower = Flower(name=name, count=count, cost=cost)
    if flowers_repository.get_flower_by_name(name=name):
        return Response(
            content=b"Flower is already exists\n",
            media_type="text/plain",
            status_code=403
        ) 

    new_flower = flowers_repository.save_flower(flower=flower)
    return {"id": new_flower.id}


@app.post("/cart/items")
def post_cart(
    flower_id: int=Form(),
    cart: str=Cookie(default="[]"),
    token: str=Depends(oauth2_scheme)
):
    flower = flowers_repository.get_flower_by_id(id=flower_id)
    cart_json = json.loads(cart)
    if flower:
        cart_json.append(flower_id)
        new_cart = json.dumps(cart_json)

    response = Response(status_code=200)
    response.set_cookie(new_cart)
    return response


# @app.get("/cart/items")
# def get_cart(token: str=Depends(oauth2_scheme)):

