from fastapi_users.authentication import JWTAuthentication

SECRET_KEY = "SdsdfsdflksfsdihfsdlkSDDFr32F@sfpsdk$fpk(eegdsda4f34d323"

auth_backends = []

jwt_authentication = JWTAuthentication(secret=SECRET_KEY, lifetime_seconds=3600)

auth_backends.append(jwt_authentication)
