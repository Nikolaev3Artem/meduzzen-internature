from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alchemy.repos.user import UserRepos
from tests.constants import (
    test_user_create_email,
    test_user_create_username,
    user_create_scheme,
    user_update_scheme,
    users_list,
)


async def test_user_get_list(users, session: AsyncSession):
    test_user_data = await UserRepos.list_users(session=session, limit=3, offset=0)
    assert len(test_user_data) == 3
    for index, user in enumerate(test_user_data):
        assert user.username == users_list[index]["username"]
        assert user.email == users_list[index]["email"]


async def test_user_create(users, session: AsyncSession):
    test_user_data = await UserRepos.create_user(user_create_scheme, session)
    assert test_user_create_email == test_user_data.email
    assert test_user_create_username == test_user_data.username


async def test_user_update(users, session: AsyncSession):
    test_user_data = await UserRepos.update_user(
        user_id=users[0].id, user_data=user_update_scheme, session=session
    )
    assert user_update_scheme.username == test_user_data.username


async def test_user_delete(users, session: AsyncSession):
    await UserRepos.deactivate_user(user_id=users[0].id, session=session)
    test_users_list = await UserRepos.list_users(session=session, limit=1, offset=0)
    assert users[0].id not in test_users_list
