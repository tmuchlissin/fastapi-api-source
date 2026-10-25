import json
from fastapi import APIRouter, HTTPException, Path as PathParameter, Query
from . import constants

router = APIRouter()

# GET API to retrieve all users from the JSON data file    
@router.get('/get-users')
async def get_list_users():
    """Return the **complete user list** from the JSON file.
    
    - **Input:** Send **GET** with no path parameter, query parameter, or request body.
    - **Action:** Read every stored user.
    - **Response:** Return the complete list in one response.
    
    **Use case:**
    
    - Export or review a small dataset when every user record is needed.
    
    **When to choose:**
    
    - Choose this route for a **complete list** with no filtering.
    - Choose the query-parameter route for search or pagination; it transfers only the requested page.
    """
    with open(constants.FILE_PATH, 'r') as file:
        data = json.load(file)
        
    return {'message' : 'Test get API successful!', 'data': data}


# GET API to retrieve a user by ID using a path parameter
@router.get('/path-variables/get-users/{user_id}')
async def get_user_by_path_var(
    user_id: int = PathParameter(
        ge=1,
        description="One-based position of the user in the practice JSON file",
    ),
):
    """Return **one user** selected by a path parameter.
    
    - **Input:** Put the one-based ``user_id`` in the URL.
    - **Validation:** A position outside the list returns **404**.
    - **Response:** Return that user's record and ``user_id``. Deletions can change later positions.
    
    **Use case:**
    
    - Open the detail page for a specific user whose position is known.
    
    **When to choose:**
    
    - Choose a **path parameter** when the request targets one known user.
    - Choose query parameters for searching, combining filters, or paginating a list.
    """
    if not constants.FILE_PATH.exists():
        raise HTTPException(status_code=404, detail="User not found")

    with open(constants.FILE_PATH, 'r') as file:
        data = json.load(file)

    user_index = user_id - 1
    if user_index >= len(data):
        raise HTTPException(status_code=404, detail="User not found")

    return {
        'message': 'User retrieved successfully!',
        'user_id': user_id,
        'data': data[user_index],
    }

# GET API to retrieve users using an optional query parameter
@router.get('/query-parameters/get-users')
async def get_user_by_query_params(
    user_id: int | None = Query(default=None, ge=1),
    name: str | None = Query(default=None, min_length=1),
    min_age: int | None = Query(default=None, ge=0),
    max_age: int | None = Query(default=None, ge=0),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
):
    """**Filter and paginate** the user list with query parameters.
    
    - **Input:** Use optional ``user_id``, ``name``, ``min_age``, and ``max_age`` filters; ``offset`` and ``limit`` select a page.
    - **Validation:** Invalid parameter values return **422**; ``min_age`` above ``max_age`` returns **400**.
    - **Action:** Apply filters before taking the requested page.
    - **Response:** Return matching users, total matches, and ``next_offset`` when more results exist.
    
    **Use case:**
    
    - Build a searchable user directory that loads a few matching records at a
      time.
    
    **When to choose:**
    
    - Choose this route for **filtering or pagination**; the client must manage ``offset`` and ``limit``.
    - Choose the path route for one known user or the full-list route for a small complete dataset.
    """
    with open(constants.FILE_PATH, 'r') as file:
        data = json.load(file)

    if min_age is not None and max_age is not None and min_age > max_age:
        raise HTTPException(
            status_code=400,
            detail='min_age cannot be greater than max_age',
        )

    users = [
        {'user_id': index, **user}
        for index, user in enumerate(data, start=1)
    ]

    if user_id is not None:
        users = [user for user in users if user['user_id'] == user_id]

    if name is not None:
        users = [
            user for user in users
            if name.lower() in user['name'].lower()
        ]

    if min_age is not None:
        users = [user for user in users if user['age'] >= min_age]

    if max_age is not None:
        users = [user for user in users if user['age'] <= max_age]

    if user_id is not None and not users:
        raise HTTPException(status_code=404, detail='User not found')

    total = len(users)
    paginated_users = users[offset:offset + limit]
    next_offset = offset + limit if offset + limit < total else None

    return {
        'message': 'Users retrieved successfully!',
        'filters': {
            'user_id': user_id,
            'name': name,
            'min_age': min_age,
            'max_age': max_age,
        },
        'pagination': {
            'offset': offset,
            'limit': limit,
            'total': total,
            'returned': len(paginated_users),
            'has_more': next_offset is not None,
            'next_offset': next_offset,
        },
        'data': paginated_users,
    }
