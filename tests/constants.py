from app.db.alchemy.models import User
from app.schemas.user import UserSignUp, UserUpdate

user = User(
    email="qwe@gmail.com",
    username="test_username",
    password="test_password",
)
updated_username = User(username=f"updated_{user.username}")

user_create_scheme = UserSignUp(
    email=user.email, password=user.password, username=user.username
)
user_update_scheme = UserUpdate(username=updated_username.username)
