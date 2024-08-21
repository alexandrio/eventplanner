from fastapi import APIRouter, HTTPException, status, Depends
from models.users import User, UserSignIn, TokenResponse

from database.connection import Database

from auth.hash_password import HashPassword
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import crate_access_token
 


user_router = APIRouter(
    tags=["User"]
)

users ={}
user_database = Database(User)

hash_password = HashPassword()


@user_router.post("/signup")
async def sign_new_user(user: User)-> dict:
    user_exist = await User.find_one(User.email==user.email)
    #if data.email in users:
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exists"
        )
        
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    #users[data.email] = data
    await user_database.save(user)
    
    return{
        "message": "User successfully registered!"
    
    }
    
    
@user_router.post("/signin")
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends(), response_model=TokenResponse) -> dict:
    user_exist = await User.find_one(User.email == user.username)
    
    
    #if user.email not in users:

    if not user_exist:    
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exists"
        )
        
        
    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = crate_access_token(user_exist.email)
        return{
            "access_token": access_token, "token_type": "Bearer"
        }
    
    #if users[user.email].password != user.password:
    if user_exist.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="wrong credentials passed"
        )
        
    return{
        "message":"User signed in successfully"
    }
        