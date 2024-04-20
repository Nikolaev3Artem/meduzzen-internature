from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alchemy.repos.user import UserRepos
from tests.constants import (
    test_user_create_email,
    test_user_create_username,
    user_create_scheme,
    user_update_scheme,
    users,
)


async def test_user_get_list(prepare_database, fill_database, session: AsyncSession):
    test_user_data = await UserRepos.list_users(session=session, limit=3, offset=0)
    assert len(test_user_data) == 3
    for i in range(len(users)):
        assert test_user_data[i].username == users[i]["username"]
        assert test_user_data[i].email == users[i]["email"]


async def test_user_create(prepare_database, fill_database, session: AsyncSession):
    test_user_data = await UserRepos.create_user(user_create_scheme, session)
    assert test_user_create_email == test_user_data.email
    assert test_user_create_username == test_user_data.username


async def test_user_update(prepare_database, fill_database, session: AsyncSession):
    test_users_list = await UserRepos.list_users(session=session, limit=1, offset=0)
    test_user_id = test_users_list[0].id
    test_user_data = await UserRepos.update_user(
        id=test_user_id, user=user_update_scheme, session=session
    )
    assert user_update_scheme.username == test_user_data.username


async def test_user_delete(prepare_database, fill_database, session: AsyncSession):
    test_users_list = await UserRepos.list_users(session=session, limit=1, offset=0)
    test_user_id = test_users_list[0].id
    await UserRepos.delete_user(id=test_user_id, session=session)
    test_users_list = await UserRepos.list_users(session=session, limit=1, offset=0)
    assert test_user_id not in test_users_list
