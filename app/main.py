from fastapi import FastAPI
from routes.advert import router as adverts_router
from basic_auth.views import router as auth_router

app = FastAPI()


app.include_router(adverts_router, prefix='/api')
app.include_router(auth_router, prefix='/auth')

@app.get('/')
async def main_page():
    return {'message':'App started'}



