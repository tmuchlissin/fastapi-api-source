import json
from fastapi import APIRouter, File, Form, UploadFile
from typing import Annotated
from app.schemas.user import User
from . import constants

router = APIRouter()

# POST API to add a new user using raw body data
@router.post('/body/raw/add-user')
async def create_user_json(user: User):
    """Create and save a user from a **JSON request body**.
    
    - **Input:** Send ``application/json`` with ``name`` (string), ``age`` (integer), and ``email`` (string).
    - **Validation:** FastAPI checks the body against the ``User`` schema. Invalid or missing fields return **422**.
    - **Action:** Append the validated user to the JSON data file.
    - **Response:** Return the complete, updated user list.
    
    **Use case:**
    
    - A frontend, mobile app, or another service needs to create a user using
      structured data.
    
    **When to choose:**
    
    - Choose **JSON** for structured API requests without file uploads.
    - Choose **form fields** for a traditional text-only form.
    - Choose **multipart/form-data** when the request includes a file.
    - This endpoint **saves** the user; the URL-encoded example only echoes submitted values.
    """
    if constants.FILE_PATH.exists():
        with open(constants.FILE_PATH, 'r') as file:
            data = json.load(file)
    else:
        data = []
        
    data.append(user.model_dump())
    
    with open(constants.FILE_PATH, 'w') as file:
        json.dump(data, file)

    return {'message': 'Test post API successful!', 'data': data}

# POST API to add a new user using form data (support both multipart/form-data and application/x-www-form-urlencoded)
@router.post('/body/form/add-user')
async def create_user_form(
    name: Annotated[str, Form()],
    age: Annotated[int, Form()],
    email: Annotated[str, Form()],
):
    """Create and save a user from **text-based form fields**.

    - **Input:** Accept ``name``, ``age``, and ``email`` using either
      ``application/x-www-form-urlencoded`` or ``multipart/form-data``.
    - **Validation:** All fields are required. FastAPI validates their declared
      types and converts ``age`` to an integer before running this function.
    - **Action:** Create a user record and append it to the JSON data file.
    - **Response:** Return a success message and the complete updated user list.

    **Use case:**

    - Save data submitted by a traditional HTML form, registration page, or
      another client that sends simple text fields instead of a JSON object.

    **When to choose:**

    - Choose this endpoint for **text-only form fields** that must be saved.
    - Prefer the JSON endpoint for structured or nested API payloads.
    - Prefer the multipart upload endpoint when the request includes a file.
    - Unlike the URL-encoded demonstration endpoint, this endpoint persists
      the submitted user instead of only echoing the values.
    """
    if constants.FILE_PATH.exists():
        with open(constants.FILE_PATH, 'r') as file:
            data = json.load(file)
    else:
        data = []
        
    data.append({
        "name": name,
        "age": age,
        "email": email
    })
    
    with open(constants.FILE_PATH, 'w') as file:
        json.dump(data, file)

    return {'message': 'Test post API successful!', 'data': data}


# POST API to add a new user using form data application/x-www-form-urlencoded.
@router.post('/body/urlencoded/add-user')
async def create_user_urlencoded(
    name: str = Form(),
    age: int = Form(),
    email: str = Form(),
):
    """
    Receive **URL-encoded form fields** without saving them.

    - **Input:** Send `name`, `age`, and `email` as form fields.
    - **Validation:** All three fields are required; `age` must be an integer.
    - **Action:** Parse the fields without saving a user.
    - **Response:** Echo the submitted values.

    **Use case:**

    - Inspect a small text-only form when the values do not need to be saved.

    **When to choose another route:**

    - Use the general form route when the user must be **saved**.
    - Use the multipart upload route when the request includes a file.

    This route also accepts text-only multipart requests because it uses FastAPI `Form` parameters.
    """
    return {
        'message': 'URL-encoded user received successfully!',
        'user': {'name': name, 'age': age, 'email': email},
    }


# POST API to add a new user using form data multipart/form-data.
@router.post('/body/multipart/add-user')
async def create_user_multipart(
    name: str = Form(),
    age: int = Form(),
    email: str = Form(),
    avatar: UploadFile = File(),
):
    """Receive user fields and an **avatar upload** in one request.
    
    - **Input:** Send ``name``, ``age``, and ``email`` as text fields and ``avatar`` as a file using ``multipart/form-data``.
    - **Validation:** FastAPI requires all fields, including the file.
    - **Action:** Read file metadata without saving the user or the file.
    - **Response:** Return the user values, filename, and file content type.
    
    **Use case:**
    
    - Submit profile details together with an avatar or another file.
    
    **When to choose:**
    
    - Choose **multipart/form-data** when a request contains a file and text fields.
    - Choose JSON or a text-only form when there is no file. The other creation examples can save users; this example only echoes data.
    """
    return {
        'message': 'Multipart user received successfully!',
        'user': {'name': name, 'age': age, 'email': email},
        'file': {
            'filename': avatar.filename,
            'content_type': avatar.content_type,
        },
    }
