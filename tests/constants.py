from app.core.hashing import Hasher
from app.db.alchemy.models import User
from app.schemas.user import UserSignUp, UserUpdate

users = [
    {
        "email": "qwe@gmail.com",
        "username": "test_username",
        "password": Hasher.get_password_hash("test_password"),
    },
    {
        "email": "qwe2@gmail.com",
        "username": "test_username",
        "password": Hasher.get_password_hash("test_password2"),
    },
    {
        "email": "qwe3@gmail.com",
        "username": "test_username",
        "password": Hasher.get_password_hash("test_password3"),
    },
]

user_create = User(
    email="qwe4@gmail.com",
    username="test_username",
    password=Hasher.get_password_hash("test_password4"),
)

updated_username = "updated_test_username"
user_bad_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"

test_user_create_email = user_create.email
test_user_create_password = user_create.password
test_user_create_username = user_create.username

user_create_scheme = UserSignUp(
    email=user_create.email,
    password=user_create.password,
    username=user_create.username,
)
user_update_scheme = UserUpdate(username=updated_username)
