from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserModel
from libgravatar import Gravatar


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieves the user selected by certain email.

    :param email: The user to retrieve.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: A user.
    :rtype: User
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new user.

    :param body: The data for the user to create.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The newly created user.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Updates a token.

    :param user: The user to update the token for.
    :type user: User
    :param token: The token of the user.
    :type token: str | None
    :param db: The database session.
    :type db: Session
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Confirmed an email.

    :param email: The email to confirm.
    :type email: str
    :param db: The database session.
    :type db: Session
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    Updates an avatar.

    :param email: The email of the user.
    :type email: str
    :param url: The url to get the avatar.
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: The user to update the avatar for.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user    
    