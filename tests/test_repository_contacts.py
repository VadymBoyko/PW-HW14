import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User, Contact
from src.schemas import ContactModel
from src.repository.contacts import create, remove, update, get_contacts, get_contact_by_id, get_contact_by_email, \
    get_contact_by_firstname, get_contact_by_lastname, get_next_week_birthday_contacts


class TestContactRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, email='test@test.com')

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query(Contact).join().filter().all.return_value = contacts
        result = await get_contacts(self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        body = ContactModel(
            firstname='Taras',
            lastname='Shevchenko',
            birthday='1814-03-09 00:00:00',
            phone='+380501234567',
            email='taras@ukraine.ua',
            notes='Просив поховати, як умре'
        )
        result = await create(self.session, self.user, body)
        self.assertEqual(result.email, body.email)
        self.assertTrue(hasattr(result, 'id'))

    async def test_update_contact(self):
        body = ContactModel(
            firstname='Taras',
            lastname='Shevchenko',
            birthday='1814-03-09 00:00:00',
            phone='+380509999999',
            email='taras@ukraine.ua',
            notes='Просив поховати, як умре'
        )
        result = await update(self.session, self.user, 1, body)
        self.assertEqual(result.email, body.email)
        self.assertTrue(hasattr(result, 'id'))

    async def test_remove_contact(self):
        result = await remove(self.session, self.user, 1)
        self.assertTrue(hasattr(result, 'id'))

    async def test_get_contact_by_id(self):
        result = await get_contact_by_id(self.session, self.user, 1)
        self.assertTrue(hasattr(result, 'id'))

    async def test_get_contact_by_email(self):
        result = await get_contact_by_email(self.session, self.user, 'taras@ukraine.ua')
        self.assertTrue(hasattr(result, 'id'))

    async def test_get_contact_by_firstname(self):
        result = await get_contact_by_firstname(self.session, self.user, 'Taras')
        self.assertTrue(hasattr(result, 'id'))

    async def test_get_contact_by_lastname(self):
        result = await get_contact_by_lastname(self.session, self.user, 'Shevchenko')
        self.assertTrue(hasattr(result, 'id'))

    async def test_get_next_week_birthday_contacts(self):
        result = await get_next_week_birthday_contacts(self.session, self.user)
        self.assertTrue(hasattr(result, 'id'))
