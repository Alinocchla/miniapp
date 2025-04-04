# pip install fastapi pydantic uvicorn sqlalchemy
# aiosqlite
# здесь отлавливаем эндпоинды
from contextlib import asynccontextmanager

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import init_db
import requests as rq


# синхронизация с БД
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db
    print('Bot is ready')
    yield


# lifespan - при запуске приложения запускается функция
app = FastAPI(title='To Do App', lifespan=lifespan)

# спец инструкции, которые вызываются до обработки какого-то события
app.add_middleware(
    CORSMiddleware,  # для безопасности, чтоб пост запросы пришли неподделанные
    allow_origins=['*'],  # url адреса, с которых разрешется приход пост запросов
    # все нужно для безопасности
    allow_credentials=True,  #
    allow_methods=["*"],  # какие методы пост/гет
    allow_headers=["*"],  # какие хедеры м. приходить(напр. толькос токенами или от определенных устройств)
)


@app.get("/api/tasks/{tg_id}")
async def tasks(tg_id: int):
    user = await rq.add_user(tg_id)
    # чтобы достать вернуть таски на фронтед,
    # нужно использовать сериализацию данных
    # т.к. JS принимает в себя данные в виде
    # json формата
    # поэтому скалярный пайтоновский объект преобразуем
    # в json формат который понимает JS
    # для этого используем pydantic
    return await rq.get_tasks(user.id)


@app.get("/api/main/{tg_id}")
async def profile(tg_id: int):
    user = await rq.add_user(tg_id)
    completed_task_count = await rq.get_completed_tasks_count(user.id)
    return {'completedTasks': completed_task_count}
