import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel, ContactUpdate, ContactStatusUpdate
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User()

    async def test_get_user_by_email(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email=user.email, db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        user = User()
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email=user.email, db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        body = UserModel(username='test_first_name', email='test@email.com',
                          password='test_pass')
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password) 
        self.assertTrue(hasattr(result, "id"))
       
    async def test_update_token_found(self):
        user = User()
        self.session.query().filter().first.return_value = user
        self.session.commit.return_value = None
        token='qwerty'
        await update_token(user=user, token=token, db=self.session)
        self.assertTrue(user.refresh_token)
        self.assertEqual(user.refresh_token, token)

    async def test_confirmed_email(self):
        user = User()
        self.session.query().filter().first.return_value = user
        self.session.commit.return_value = None
        email='test@email.com'
        await confirmed_email(email=email, db=self.session)
        self.assertTrue(user.confirmed)

    async def test_update_avatar(self):
        user = User()
        self.session.query().filter().first.return_value = user
        url = 'http'
        await update_avatar(email=user.email, url=url, db=self.session)
        self.assertTrue(user.avatar)


if __name__ == '__main__':
    unittest.main()
