from fastapi import FastAPI
from routes.advert import router as adverts_router

app = FastAPI()


app.include_router(adverts_router)

@app.get('/')
async def main_page():
    return {'message':'App started'}



