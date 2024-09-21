from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()

mail = str(os.environ.get("mail"))
password = str(os.environ.get("password"))


@dataclass
class AuthData:
    mail: str
    password: str


config = AuthData(mail=mail, password=password)
