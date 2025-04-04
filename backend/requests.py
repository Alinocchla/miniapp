from sqlalchemy import (
    select,
    update,
    delete,
    func,
)
from models import (
    async_session,
    User,
    Task,
)
from pydantic import (
    BaseModel,
    ConfigDict,
)
from typing import List


class TaskSchema(BaseModel):  # аналогичен class Task(Base)
    id: int
    title: str
    completed: bool
    user: int

    # чтобы сериализация работала корректно:
    model_config = ConfigDict(from_attributes=True)


# запросы к БД
async def add_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user

        new_user = User(tg_id=tg_id)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


async def get_tasks(user_id):
    async with async_session() as session:
        tasks = await session.scalars(
            select(Task).where(Task.user == user_id, Task.completed == False)
        )
        # сериализация данных
        # из питоновского типа преобразуем в тот, который можем передать
        # по JSON и при этом, чтобы JS его понимал
        serialized_tasks = [
            TaskSchema.model_validate(t).model_dump() for t in tasks
        ]
        # данные которые можем передать на фронтед и он их поймет
        return serialized_tasks


# отображаем сколько выполненных тасков у юзера
async def get_completed_tasks_count(user_id):
    async with async_session() as session:
        return await session.scalar(select(func.count(Task.id)).where(Task.completed == True))


async def add_task(user_id, title):
    async with async_session() as session:
        new_task = Task(
            title=title,
            user=user_id
        )
        session.add(new_task)
        await session.commit()


async def update_task(task_id):
    async with async_session() as session:
        await session.execute(update(Task).where(Task.id == task_id).values(completed=True))
        await session.commit()
