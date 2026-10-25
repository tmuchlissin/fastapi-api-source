import json
from secrets import compare_digest
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.config.core import settings
from app.schemas.user import User
from . import constants

router = APIRouter()
bearer_security = HTTPBearer()

def verify_bearer_token(
    credentials: HTTPAuthorizationCredentials = Security(bearer_security),
) -> str:
    """Check the practice bearer token for routes that require authentication.

    FastAPI reads the Authorization header through HTTPBearer. A missing or
    incorrect token returns 401; a valid token lets the endpoint continue.
    """
    if not compare_digest(
        credentials.credentials,
        settings.TEST_BEARER_TOKEN,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid bearer token',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return credentials.credentials

# GET API to check a bearer token sent in the Authorization header
@router.get('/auth/bearer')
async def authenticate_with_bearer_token(
    verified_token: str = Depends(verify_bearer_token),
):
    """Check a **bearer token** without changing user data.
    
    - **Input:** Send a token in the ``Authorization: Bearer <token>`` header.
    - **Validation:** The token must match the configured practice token.
    - **Response:** Return a confirmation for a valid token; missing or invalid tokens return **401**.
    
    **Use case:**
    
    - Confirm that a client has a valid credential before it calls a protected
      endpoint.
    
    **When to choose:**
    
    - Choose this **GET** to check access without creating a user.
    - A successful check does not log the client in; each protected request must send the token again.
    """
    return {
        'message': 'Authentication successful!',
        'scheme': 'Bearer',
    }


# POST API to add a user using a bearer token and JSON body
@router.post(
    '/auth/bearer/add-user',
    status_code=status.HTTP_201_CREATED,
)
async def create_user_with_bearer_token(
    user: User,
    verified_token: str = Depends(verify_bearer_token),
):
    """Create a user with a **bearer token** and a **JSON body**.
    
    - **Input:** Send ``Authorization: Bearer <token>`` and JSON containing ``name``, ``age``, and ``email``.
    - **Validation:** The token must be valid, and the body must match the ``User`` schema.
    - **Action:** Append the user to the JSON data file only after authentication succeeds.
    - **Response:** Return the created user with **201**; missing or invalid tokens return **401**.
    
    **Use case:**
    
    - Allow only authorized clients to add users.
    
    **When to choose:**
    
    - Choose this route when creating a user requires authentication.
    - The JSON creation example accepts the same user body without requiring a bearer token.
    """
    if constants.FILE_PATH.exists():
        with open(constants.FILE_PATH, 'r') as file:
            data = json.load(file)
    else:
        data = []

    created_user = user.model_dump()
    data.append(created_user)

    with open(constants.FILE_PATH, 'w') as file:
        json.dump(data, file, indent=2)

    return {
        'message': 'Authenticated user created successfully!',
        'data': created_user,
    }
