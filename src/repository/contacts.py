from datetime import datetime, timedelta

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(db: Session, user: User):
    """
    The get_contacts function returns a list of contacts for the user.

    :param db: Session: Pass the database session to the function
    :param user: User: Get the user id from the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = db.query(Contact).join(User).filter(User.id == user.id).all()
    return contacts


async def get_contact_by_id(db: Session, user: User, contact_id: int):
    """
    The get_contact_by_id function returns a contact by its id.
        Args:
            db (Session): The database session to use for the query.
            user (User): The user who is making the request. This is used to ensure that only contacts belonging to this user are returned.
            contact_id (int): The id of the contact being requested.

    :param db: Session: Connect to the database
    :param user: User: Get the user's id from the database
    :param contact_id: int: Get the contact by id
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).join(User).filter(and_(Contact.id == contact_id, User.id == user.id)).first()
    return contact


async def get_next_week_birthday_contacts(db: Session, user: User):
    """
    The get_next_week_birthday_contacts function returns a list of contacts whose birthday is within the next week.

    :param db: Session: Pass in the database session
    :param user: User: Filter the contacts by user
    :return: A list of contacts that have a birthday within the next week
    :doc-author: Trelent
    """
    today = datetime.today()
    next_week = today + timedelta(days=7)
    contacts = db.query(Contact).join(User).filter(
        and_(
            func.to_char(Contact.birthday, 'MM-DD') >= func.to_char(today, 'MM-DD'),
            func.to_char(Contact.birthday, 'MM-DD') <= func.to_char(next_week, 'MM-DD'),
            User.id == user.id
        )
    ).all()
    return contacts


async def get_contact_by_email(db: Session, user: User, email: str):
    """
    The get_contact_by_email function returns a contact object from the database based on the email address provided.
        Args:
            db (Session): The SQLAlchemy session to use for querying.
            user (User): The user who owns the contact being retrieved. This is used to ensure that only contacts owned by this user are returned, and not those of other users in the system.
            email (str): The email address of the contact being retrieved.

    :param db: Session: Pass in the database session
    :param user: User: Get the user id from the user table
    :param email: str: Filter the database query by email
    :return: The contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).join(User).filter(
        and_(Contact.email.ilike(email),
             User.id == user.id)).first()
    return contact


async def get_contact_by_firstname(db: Session, user: User, firstname: str):
    """
    The get_contact_by_firstname function returns a list of contacts that match the firstname parameter.
        The user parameter is used to filter the results by user id.

    :param db: Session: Connect to the database
    :param user: User: Get the user id from the database
    :param firstname: str: Filter the contacts by firstname
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = db.query(Contact).join(User).filter(
        and_(Contact.firstname.ilike(firstname),
             User.id == user.id)).all()
    return contacts


async def get_contact_by_lastname(db: Session, user: User, lastname: str):
    """
    The get_contact_by_lastname function returns a list of contacts that match the lastname parameter.
        The user parameter is used to filter the results by user id.

    :param db: Session: Pass the database session to the function
    :param user: User: Get the user id from the database
    :param lastname: str: Filter the contacts by lastname
    :return: A list of contacts with the same lastname
    :doc-author: Trelent
    """
    contacts = db.query(Contact).join(User).filter(
        and_(Contact.lastname.ilike(lastname),
             User.id == user.id)).all()
    return contacts


async def create(db: Session, user: User, body: ContactModel):
    """
    The create function creates a new contact in the database.


    :param db: Session: Access the database
    :param user: User: Get the user_id from the user object
    :param body: ContactModel: Get the data from the request body
    :return: A contact object
    :doc-author: Trelent
    """
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(db: Session, user: User, contact_id: int, body: ContactModel):
    """
    The update function updates a contact in the database.
        Args:
            db (Session): The database session to use for updating the contact.
            user (User): The user who is making this request. This is used to ensure that only contacts belonging to this user are updated.
            contact_id (int): The id of the contact being updated, which must belong to the specified user or an error will be raised and no update will occur.
                If no such id exists, then an error will be raised and no update will occur.

    :param db: Session: Access the database
    :param user: User: Identify the user
    :param contact_id: int: Identify the contact to be deleted
    :param body: ContactModel: Update the contact
    :return: The contact object
    :doc-author: Trelent
    """
    contact = await get_contact_by_id(db, user, contact_id)
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.phone = body.phone
        contact.email = body.email
        contact.birthday = body.birthday
        contact.notes = body.notes
        db.commit()
    return contact


async def remove(db: Session, user: User, contact_id: int):
    """
    The remove function removes a contact from the database.
        Args:
            db (Session): The database session to use for querying.
            user (User): The user who is making the request. This is used to ensure that only contacts belonging to this user are removed.
            contact_id (int): The id of the contact being removed.

    :param db: Session: Pass the database session to the function
    :param user: User: Get the user's id and use it to find the contact
    :param contact_id: int: Specify the contact to be removed
    :return: The contact that was removed
    :doc-author: Trelent
    """
    contact = await get_contact_by_id(db, user, contact_id)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
