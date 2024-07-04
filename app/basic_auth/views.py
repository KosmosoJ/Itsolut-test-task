from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from fastapi.security import  HTTPBasic, HTTPBasicCredentials

router = APIRouter()

security = HTTPBasic()



def get_auth_user(user_info:Annotated[HTTPBasicCredentials, Depends(security)]):
    if user_info.username == 'admin':
        if user_info.password == 'admin':
            return user_info.username
        else:
            raise HTTPException(401, 'Not found username or password')
    else:
        raise HTTPException(401, 'Not found username or password')
    
@router.get('/basic-auth/')
async def basic_auth(user_info:Annotated[str, Depends(get_auth_user)]):
    return{'message':'hi',
           'username':user_info}
