from starlette.requests import Request
from .schemas import UserDB


# def on_after_register(user: UserDB, request: Request):
#     print(f"User {user.id} has registered")
from .services import send_email


def send_sms_code(user: UserDB, request: Request) -> None:
    print(f"User {user.id} has registered. {123456}")


def send_email_code(user: UserDB, request: Request) -> None:
    print(f"User {user.id} has registered. {123456}")


def send_email_after_register(user: UserDB, request: Request):
    message = f'Hello! {user.username}'
    subscription = 'Hello!'
    send_email(message=message, to_address=user.email, subscription=subscription)


def after_verification(user: UserDB, request: Request) -> None:
    print(f"{user}")


def after_verification_request(user: UserDB, token: str, request: Request) -> None:
    print(f"{user} --- {token}")