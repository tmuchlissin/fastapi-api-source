import json
from fastapi import APIRouter, File, Form, UploadFile
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
    name: str = Form(), 
    age: int = Form(), 
    email: str = Form()
    ):
    """Create and save a user from **text form fields**.
    
    - **Input:** Send ``name``, ``age``, and ``email`` as URL-encoded or multipart form fields.
    - **Validation:** FastAPI requires all three fields and parses ``age`` as an integer.
    - **Action:** Append the user to the JSON data file; this route does not accept a file.
    - **Response:** Return the complete, updated user list.
    
    **Use case:**
    
    - Save a registration submitted by a text-only form.
    
    **When to choose:**
    
    - Choose this route for form submissions that must be **stored**.
    - Choose the JSON route for a JSON body or the multipart upload route when a file is included.
    - The URL-encoded example only echoes values and does not store them.
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
