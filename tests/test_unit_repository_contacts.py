import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate, ContactStatusUpdate
from src.repository.contacts import (
    get_contacts,
    get_contact_by_birthday,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
    update_status_contact,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().all.return_value = contact
        result = await get_contact(first_name=contact.first_name, last_name=contact.last_name, email=contact.email,
                                   user=self.user, db=self.session)
        self.assertEqual(result, contact) 

    async def test_get_contact_not_found(self):
        contact = Contact()
        self.session.query().filter().all.return_value = None
        result = await get_contact(first_name=contact.first_name, last_name=contact.last_name, email=contact.email,
                                   user=self.user, db=self.session)
        self.assertIsNone(result)
    
    async def test_get_contact_by_birthday(self):
        contact = []
        self.session.query().all.return_value = contact
        result = await get_contact_by_birthday(user=self.user, db=self.session)
        self.assertEqual(result, contact)
       
    async def test_create_contact(self):
        body = ContactModel(first_name='test_first_name', last_name='test_last_name',
                             email='test@email.com', phone='test_phone',
                               birthday=23-1-1, user_id=self.user.id)
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday) 
        self.assertTrue(hasattr(result, "id"))        

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = ContactUpdate(first_name='test_first_name', last_name='test_last_name',
                             email='test@email.com', phone='test_phone',
                               birthday=23-1-1, done=True, user_id=self.user.id)
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)        

    async def test_update_contact_not_found(self):
        body = ContactUpdate(first_name='test_first_name', last_name='test_last_name',
                             email='test@email.com', phone='test_phone',
                               birthday=23-1-1, done=True, user_id=self.user.id)
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_status_contact_found(self):
        body = ContactStatusUpdate(done=True)
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_status_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_status_contact_not_found(self):
        body = ContactStatusUpdate(done=True)
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_status_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
