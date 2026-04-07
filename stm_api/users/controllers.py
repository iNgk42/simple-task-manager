from fastapi import APIRouter, HTTPException, status
from stm_api.database.mock_users_db import users_db
from stm_api.users.models import UserCreate, UserInDb, UserLogin, UserRead, UserUpdate
from stm_api.utils import hash_password

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", responses={500: {"description": "Error fetching users from database"}})
async def get_all_users():
    if not users_db:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching users from database")
    
    users_db_read = []
    for user in users_db:
        users_db_read.append(UserRead(id=user.id, name=user.name, email=user.email, created_at=user.created_at))

    return {"users": users_db_read}

@router.post(
    "/me",
    status_code=status.HTTP_200_OK, 
    responses={
        200: {"description": "User logged in successfully"},
        401: {"description": "Invalid credentials"}
    }
)
async def get_current_user(user_cresentials: UserLogin):
    for user in users_db:
        if user.email == user_cresentials.email and user.passwordhash == hash_password(user_cresentials.password):
            user_read = UserRead(id=user.id, name=user.name, email=user.email, created_at=user.created_at)
            return {"message": "User logged in successfully", "user": user_read}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("/{id}", responses={404: {"description": "User not found"}})
async def get_user_by_id(id: int):
    for user in users_db:
        if user.id == id:
            user_read = UserRead(id=user.id, name=user.name, email=user.email, created_at=user.created_at)
            return {"user": user_read}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Email already registered"}, 
        201: {"description": "User created successfully"}
    }
)
async def register_user(user: UserCreate):
    for existing_user in users_db:
        if existing_user.email == user.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    user_in_db = UserInDb(
        id = users_db[-1].id + 1 if (users_db and users_db != []) else 1,
        name = user.name,
        email = user.email,
        passwordhash = hash_password(user.password)
    )
    users_db.append(user_in_db)
    
    user_read = UserRead(
        id = user_in_db.id,
        name = user_in_db.name,
        email = user_in_db.email,
        created_at = user_in_db.created_at
    )
    return {"message": "User created successfully", "user": user_read}


@router.put(
    "/{id}", 
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "User updated successfully"},
        400: {"description": "Email already registered"},
        404: {"description": "User not found"}
    }
)
async def update_user(id: int, user_update: UserUpdate):
    for existing_user in users_db:
        if existing_user.email == user_update.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    for index, user in enumerate(users_db):
        if user.id == id:
            if user_update.name != "":
                user.name = user_update.name
            if user_update.email != "":
                user.email = user_update.email 
            if user_update.password != "":
                user.passwordhash = hash_password(user_update.password)

            users_db[index] = user

            user_read = UserRead(
                id=users_db[index].id,
                name=users_db[index].name,
                email=users_db[index].email,
                created_at=users_db[index].created_at
            )
            return {"message": "User updated successfully", "user": user_read}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.delete(
    "/{id}", 
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "User not found"},
        200: {"description": "User deleted successfully"}
    }
)
async def delete_user(id: int):
    for index, user in enumerate(users_db):
        if user.id == id:
            del users_db[index]
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")