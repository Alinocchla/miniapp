# описываем сущности
from sqlalchemy import (
    ForeignKey,
    String,
    BigInteger,
)
from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column,
)
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)

# используем не серверную, а файловую БД
engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=True)

# запросы в БД
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


'''
Класс - сущность
Класс называется в единственном числе, а таблица - во множественном.
Потому что с помощью одного класса мы описываем одного пользователя,
описываем сущность одного человека, а в таблице будут хранится множество
сущностей.
'''


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    completed: Mapped[bool] = mapped_column(default=False)
    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
