import uvicorn
from fastapi import FastAPI, APIRouter

from database.base import database
from endpoints.user_endpoint import router as user_router
from endpoints.package_endpoint import router as package_router
from endpoints.authorization import router as token_router

app = FastAPI()
app.include_router(user_router,prefix='/user', tags = ['user'])
app.include_router(package_router, prefix='/package', tags = ['package'])
app.include_router(token_router, prefix='/token', tags = ['tokens'])


@app.get('/')
async def home():
    return {'run': 'true'}

@app.on_event('startup')
async def connect_db():
    await database.connect()

@app.on_event('shutdown')
async def connect_db():
    await database.disconnect()

if __name__ == '__main__':
    uvicorn.run('main:app', port=8080, reload=True)