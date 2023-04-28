from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.schemas import ContactResponse, ContactModel
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.get("/", response_model=List[ContactResponse], name="Return all contacts")
async def get_contacts(db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts for the current user.

    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(db, current_user)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, name="Return contact by id")
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function is a GET request that returns the contact with the given ID.
    The function takes in an optional contact_id parameter, which defaults to 1 if not provided.
    It also takes in a db Session object and current_user User object as parameters, both of which are injected by FastAPI's dependency injection system.

    :param contact_id: int: Specify the contact id that is passed in the url
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user that is currently logged in
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_id(db, current_user, contact_id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/search_by_lastname/{contact_lastname}", response_model=List[ContactResponse], name="Return contact by lastname")
async def get_contact_by_lastname(lastname: str, db: Session = Depends(get_db),
                                  current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_lastname function is used to retrieve a contact by lastname.
        The function takes in the following parameters:
            - lastname (str): The last name of the contact you are searching for.
            - db (Session, optional): A database Session object that will be used to query the database. Defaults to Depends(get_db).
            - current_user (User, optional): A User object representing the currently logged-in user making this request. Defaults to Depends(auth_service.get_current_user).

    :param lastname: str: Pass the lastname of a contact to the function
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A list of contacts with the specified lastname
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contact_by_lastname(db, current_user, lastname)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts


@router.get("/search_by_firstname/{contact_firstname}", response_model=List[ContactResponse], name="Return contact by firstname")
async def get_contact_by_firstname(firstname: str, db: Session = Depends(get_db),
                                   current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_firstname function is used to retrieve a contact by firstname.
        The function takes in the following parameters:
            - firstname (str): The first name of the contact you are searching for.
            - db (Session, optional): A database Session object that will be used to query the database. Defaults to Depends(get_db).
            - current_user (User, optional): A User object representing the currently logged-in user making this request. Defaults to Depends(auth_service.get_current_user).

    :param firstname: str: Specify the firstname of the contact we want to retrieve
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A list of contacts with the given firstname
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contact_by_firstname(db, current_user, firstname)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts


@router.get("/next_week_birthday/", response_model=List[ContactResponse], name="Return all contacts who have birthday next 7 days")
async def get_contacts(db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts that have birthdays in the next week.

    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: A list of contact objects
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_next_week_birthday_contacts(db, current_user)
    return contacts


@router.post("/", response_model=ContactResponse, name="Create contact", status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Get the data from the request body
    :param db: Session: Get the database connection
    :param current_user: User: Get the current user from the database
    :return: The contactmodel object, which is the same as the body of the request
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_email(db, current_user, body.email)
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is exists!')
    contact = await repository_contacts.create(db, current_user, body)
    return contact


@router.put("/{contact_id}", name="Update contact by id", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id and a body as input, which is then used to update the contact.
        If no such contact exists, it returns 404 Not Found.

    :param body: ContactModel: Validate the request body
    :param contact_id: int: Specify the contact id to be updated
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the current user from the database
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.update(db, current_user, contact_id, body)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", name="Delete contact by id", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.

    :param contact_id: int: Identify the contact to be removed
    :param db: Session: Get the database session
    :param current_user: User: Get the user that is currently logged in
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove(db, current_user, contact_id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
