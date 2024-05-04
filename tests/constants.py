from app.core.enums import RequestStatus
from app.core.hashing import Hasher
from app.db.alchemy.models import User
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.schemas.quiz import QuizCreate
from app.schemas.user import UserSignIn, UserSignUp, UserUpdate

users_list = [
    {
        "email": "qwe@gmail.com",
        "username": "test_username1",
        "password": Hasher.get_password_hash("test_password"),
    },
    {
        "email": "qwe2@gmail.com",
        "username": "test_username2",
        "password": Hasher.get_password_hash("test_password2"),
    },
    {
        "email": "qwe3@gmail.com",
        "username": "test_username3",
        "password": Hasher.get_password_hash("test_password3"),
    },
    {
        "email": "qwe5@gmail.com",
        "username": "test_username5",
        "password": Hasher.get_password_hash("test_password5"),
    },
    {
        "email": "qwe6@gmail.com",
        "username": "test_username6",
        "password": Hasher.get_password_hash("test_password6"),
    },
]
companies_list = [
    {"name": "test1", "description": "test_desc1"},
    {"name": "test2", "description": "test_desc2"},
    {"name": "test3", "description": "test_desc3"},
]

requests = [
    {"status": RequestStatus.INVITATION.value},
    {"status": RequestStatus.JOIN_REQUEST.value},
    {"status": RequestStatus.MEMBER.value},
    {"status": RequestStatus.ADMIN.value},
]

quiz_list = [
    {
        "name": "quiz_1",
        "description": "quiz_desc_1",
        "questions": [
            {
                "name": "3",
                "answers": [
                    {"name": "1", "is_correct": False},
                    {"name": "2", "is_correct": True},
                ],
            },
            {
                "name": "321",
                "answers": [
                    {"name": "2", "is_correct": False},
                    {"name": "2", "is_correct": True},
                ],
            },
        ],
    },
    {
        "name": "quiz_2",
        "description": "quiz_desc_2",
        "questions": [
            {
                "name": "3",
                "answers": [
                    {"name": "1", "is_correct": False},
                    {"name": "2", "is_correct": True},
                ],
            },
            {
                "name": "321",
                "answers": [
                    {"name": "2", "is_correct": False},
                    {"name": "2", "is_correct": True},
                ],
            },
        ],
    },
    {
        "name": "quiz_3",
        "description": "quiz_desc_3",
        "questions": [
            {
                "name": "3",
                "answers": [
                    {"name": "1", "is_correct": False},
                    {"name": "2", "is_correct": True},
                ],
            },
            {
                "name": "321",
                "answers": [
                    {"name": "2", "is_correct": False},
                    {"name": "2", "is_correct": True},
                ],
            },
        ],
    },
]

quiz_create = QuizCreate(
    name=quiz_list[0]["name"],
    description=quiz_list[0]["description"],
    questions=quiz_list[0]["questions"],
)
quiz_create = quiz_create.model_dump()

quiz_update = {"name": "quiz_updated_name"}

test_company_create = CompanyCreate(name="test4", description="test_desc4")

test_company_create_name = test_company_create.name
test_company_create_description = test_company_create.description

company_updated_name = "New company name"
company_update_scheme = CompanyUpdate(name=company_updated_name)

updated_username = "updated_test_username"
user_bad_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"

user_create = User(
    email="qwe4@gmail.com",
    username="test_username",
    password=Hasher.get_password_hash("test_password4"),
)

test_company_owner_login = UserSignIn(
    email="qwe@gmail.com",
    password="test_password",
)

test_user_login = UserSignIn(
    email="qwe2@gmail.com",
    password="test_password2",
)

test_user_leave = UserSignIn(
    email="qwe5@gmail.com",
    password="test_password5",
)

user_create_scheme = UserSignUp(
    email=user_create.email,
    password=user_create.password,
    username=user_create.username,
)

test_user_create_email = user_create.email
test_user_create_password = user_create.password
test_user_create_username = user_create.username

user_update_scheme = UserUpdate(username=updated_username)
