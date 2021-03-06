from fastapi import APIRouter


from user.api import after_verification, send_sms_code, after_verification_request
from user.auth import jwt_authentication, fastapi_users, SECRET_KEY
from user.api import send_email_after_register

user_router = APIRouter()


user_router.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)

user_router.include_router(
    fastapi_users.get_register_router(send_email_after_register), prefix="/auth", tags=["auth"]
)

# user_router.include_router(
#     fastapi_users.get_reset_password_router(
#         SECRET, after_forgot_password=on_after_forgot_password
#     ),
#     prefix="/auth",
#     tags=["auth"],
# )

user_router.include_router(
    fastapi_users.get_verify_router(
        SECRET_KEY,
        after_verification_request=after_verification_request,
        after_verification=after_verification
    ),
    prefix="/auth",
    tags=["auth"],
)

user_router.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"]
)

