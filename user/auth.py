from fastapi_users.authentication import JWTAuthentication
from user.models import user_db
from user.schemas import UserCreate, User, UserUpdate, UserDB
from fastapi_users import FastAPIUsers


SECRET_KEY = "SdsdfsdflksfsdihfsdlkSDDFr32F@sfpsdk$fpk(eegdsda4f34d323"

auth_backends = []

jwt_authentication = JWTAuthentication(secret=SECRET_KEY, lifetime_seconds=3600)

auth_backends.append(jwt_authentication)


fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

current_active_user = fastapi_users.current_user(active=True)