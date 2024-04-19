from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alchemy.repos.user import UserRepos
from tests.constants import (
    updated_username,
    user,
    user_create_scheme,
    user_update_scheme,
)


async def test_user_create(session: AsyncSession):
    test_user_data = await UserRepos.create_user(user_create_scheme, session)
    assert user.email == test_user_data.email
    assert user.username == test_user_data.username


async def test_user_get_list(session: AsyncSession):
    test_user_data = await UserRepos.list_users(session)
    assert len(test_user_data) == 1


async def test_user_update(session: AsyncSession):
    test_users_list = await UserRepos.list_users(session)
    test_user_id = test_users_list[0][0].id
    test_user_data = await UserRepos.update_user(
        id=test_user_id, user=user_update_scheme, session=session
    )
    assert updated_username.username == test_user_data.username


async def test_user_delete(session: AsyncSession):
    test_users_list = await UserRepos.list_users(session)
    test_user_id = test_users_list[0][0].id
    await UserRepos.delete_user(id=test_user_id, session=session)
    test_users_list = await UserRepos.list_users(session)
    assert test_user_id not in test_users_list
