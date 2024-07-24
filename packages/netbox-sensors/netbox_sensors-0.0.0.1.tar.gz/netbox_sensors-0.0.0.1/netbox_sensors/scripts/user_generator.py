import random
import secrets
import string
from datetime import datetime
from typing import Dict


def generate_password(level: int = 0, password_length: int = 32) -> str:
    """
    Method to construct a password indicating the security
    level and the number of characters.

    Parameters
    ----------
    level: int
        Security level.
    password_length: int
        Number of characters that the password will have.

    Notes
    -----
    Definition of the levels that exist in this method:
    Level 0, digits only.
    Level 1, letters only.
    Level 3, digits and letters.
    Level 3, digits, letters and special characters.

    Returns
    -------
    str.
        Password generated according to the indicated configuration.
    """
    allowed_characters = str
    if level == 0:
        allowed_characters = string.digits
    if level == 1:
        allowed_characters = string.ascii_letters
    if level == 2:
        allowed_characters = string.ascii_letters + string.digits
    if level == 3:
        allowed_characters = string.ascii_letters + string.digits + string.punctuation

    generated_password = "".join(
        secrets.choice(allowed_characters) for _ in range(password_length)
    )
    return generated_password


def generate_username(first_name: str) -> str:
    """
    Generates the composite name of a user.

    Parameters
    ----------
    first_name: str
        First part of the username.

    Returns
    -------
    str.
        Returns a composite username.
    """
    seconds = datetime.now().second
    name_of_stars = [
        "Sirius",
        "Betelgeuse",
        "Proxima Centauri",
        "Alpha Centauri",
        "Vega",
        "Antares",
        "Polaris",
        "Aldebaran",
        "Arcturus",
        "Rigel",
        "Deneb",
        "Spica",
        "Altair",
        "Bellatrix",
        "Castor",
        "Pollux",
        "Regulus",
        "Algol",
        "Capella",
        "Alpheratz",
        "Fomalhaut",
        "Mizar",
        "Denebola",
        "Mintaka",
        "Mirach",
        "Adhara",
        "Wezen",
        "Scheat",
        "Menkar",
        "Thuban",
    ]
    second_name = secrets.choice(name_of_stars)
    username = f"{first_name}_{second_name}_{seconds}"
    return username.lower()


def new_rabbitmq_user(
    first_name: str, level: int = 0, password_length: int = 32
) -> Dict:
    """
    Method that returns a RabbitMQ user.

    Parameters
    ----------
    first_name: str
        First part of the username.
    level: int
        Security level.
    password_length: int
        Number of characters that the password will have.

    Returns
    -------
    Dict.
        _.
    """
    return {
        "rabbitmq": {
            "user": generate_username(first_name=first_name),
            "password": generate_password(level=level, password_length=password_length),
        }
    }
