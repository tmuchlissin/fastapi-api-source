import json
from fastapi import APIRouter, HTTPException, Path as PathParameter, Response, status
from app.schemas.user import User, UserUpdate
from . import constants

router = APIRouter()

# PUT API to replace all fields of a user using a path parameter and JSON body
@router.put('/users/{user_id}')
async def replace_user(
    user: User,
    user_id: int = PathParameter(ge=1),
):
    """Replace **all fields** of one user with **PUT**.
    
    - **Input:** Put the one-based ``user_id`` in the URL and send the complete ``User`` JSON body.
    - **Validation:** All required fields must be present; an unknown user returns **404**.
    - **Action:** Replace the stored record at that list position.
    - **Response:** Return the replacement user and its ``user_id``.
    
    **Use case:**
    
    - Save a complete profile edit when the client knows every desired field
      value.
    
    **When to choose:**
    
    - Choose **PUT** for a full replacement. Missing required fields fail validation rather than retaining old values.
    - Choose **PATCH** when only selected fields should change.
    """
    with open(constants.FILE_PATH, 'r') as file:
        data = json.load(file)

    user_index = user_id - 1
    if user_index >= len(data):
        raise HTTPException(status_code=404, detail='User not found')

    data[user_index] = user.model_dump()

    with open(constants.FILE_PATH, 'w') as file:
        json.dump(data, file, indent=2)

    return {
        'message': 'User replaced successfully!',
        'user_id': user_id,
        'data': data[user_index],
    }


# PATCH API to update selected user fields using a path parameter and JSON body
@router.patch('/users/{user_id}')
async def update_user(
    update: UserUpdate,
    user_id: int = PathParameter(ge=1),
):
    """Update **selected fields** of one user with **PATCH**.
    
    - **Input:** Put the one-based ``user_id`` in the URL and send a JSON body with the fields to change.
    - **Validation:** An empty body object returns **400**; an unknown user returns **404**.
    - **Action:** Merge supplied fields into the stored record and preserve omitted fields.
    - **Response:** Return the updated user and its ``user_id``.
    
    **Use case:**
    
    - Change a user's age or email without resending the rest of the profile.
    
    **When to choose:**
    
    - Choose **PATCH** for a partial edit.
    - Choose **PUT** when replacing the complete record with all required fields.
    """
    with open(constants.FILE_PATH, 'r') as file:
        data = json.load(file)

    user_index = user_id - 1
    if user_index >= len(data):
        raise HTTPException(status_code=404, detail='User not found')

    changes = update.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(
            status_code=400,
            detail='Provide at least one field to update',
        )

    data[user_index].update(changes)

    with open(constants.FILE_PATH, 'w') as file:
        json.dump(data, file, indent=2)

    return {
        'message': 'User updated successfully!',
        'user_id': user_id,
        'data': data[user_index],
    }


# DELETE API to remove a user using a path parameter
@router.delete(
    '/users/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int = PathParameter(ge=1),
):
    """Delete **one user** identified by a path parameter.
    
    - **Input:** Put the one-based ``user_id`` in the URL; no request body is needed.
    - **Validation:** An unknown user returns **404**.
    - **Action:** Remove that record from the JSON list. Later list positions then shift.
    - **Response:** Return **204 No Content** with an empty body on success.
    
    **Use case:**
    
    - Remove a user after an administrator confirms the deletion.
    """
    with open(constants.FILE_PATH, 'r') as file:
        data = json.load(file)

    user_index = user_id - 1
    if user_index >= len(data):
        raise HTTPException(status_code=404, detail='User not found')

    data.pop(user_index)

    with open(constants.FILE_PATH, 'w') as file:
        json.dump(data, file, indent=2)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# HEAD API to retrieve the user count in response headers
@router.head('/get-users')
async def get_users_headers():
    """Return the **user count** in a HEAD response header.
    
    - **Input:** Send **HEAD** to ``/get-users``; no request body is needed.
    - **Action:** Count the records in the JSON data file.
    - **Response:** Return ``X-Total-Count`` with no response body.
    
    **Use case:**
    
    - Show a total-user count on a dashboard without downloading the list.
    
    **When to choose:**
    
    - Choose **HEAD** when only the count is needed.
    - Choose **GET** ``/get-users`` when the client needs the user records.
    """
    with open(constants.FILE_PATH, 'r') as file:
        data = json.load(file)

    return Response(
        status_code=status.HTTP_200_OK,
        headers={'X-Total-Count': str(len(data))},
    )


# OPTIONS API to list supported methods for a user resource
@router.options('/users/{user_id}')
async def get_user_options(
    user_id: int = PathParameter(ge=1),
):
    """Show an example **OPTIONS** response for a user URL.
    
    - **Input:** Put a one-based ``user_id`` in the URL; no request body is needed.
    - **Action:** Return a fixed ``Allow`` header for this practice route.
    - **Response:** Return **204 No Content** with the advertised methods in a header.
    
    **Use case:**
    
    - Learn how an OPTIONS response can communicate available HTTP methods.
    
    **Important:**
    
    - This is a **fixed teaching example**, not a live inventory of registered routes.
    - It does not perform CORS preflight handling.
    """
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={'Allow': 'GET, PUT, PATCH, DELETE, OPTIONS'},
    )
