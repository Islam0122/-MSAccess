from sqlalchemy import DateTime, BigInteger, String, func, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Базовый класс для всех ORM моделей
# Все таблицы базы данных будут наследоваться от него
class Base(DeclarativeBase):
    pass


# Mixin для добавления поля времени создания записи
# Это поле автоматически будет добавляться в таблицы,
# которые наследуют этот класс
class TimestampMixin:
    created: Mapped[DateTime] = mapped_column(
        DateTime,
        default=func.now()  # автоматически ставит текущее время
    )


# Модель пользователя
class User(TimestampMixin, Base):
    __tablename__ = "users"  # название таблицы в базе данных
    id: Mapped[int] = mapped_column(primary_key=True) # Уникальный идентификатор пользователя в базе
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True) # Telegram ID пользователя (уникальный)
    username: Mapped[str] = mapped_column(String(255))  # Username пользователя Telegram
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user") # Связь: один пользователь может иметь много транзакций

# Модель транзакций (доходы / расходы)
class Transaction(TimestampMixin, Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)   # Уникальный ID транзакции
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id")) # ID пользователя (внешний ключ) # связывает транзакцию с таблицей users
    type: Mapped[str] = mapped_column(String(50)) # Тип транзакции (income / expense)
    amount: Mapped[int] = mapped_column(Integer) # Сумма транзакции
    category: Mapped[str | None] = mapped_column(String(255)) # Категория расхода или дохода (может быть пустой)
    description: Mapped[str | None] = mapped_column(String(255)) # Описание транзакции (например: "обед", "зарплата")
    user: Mapped["User"] = relationship(back_populates="transactions")

class Question(TimestampMixin, Base):
    __tablename__ = "questions_tezt"
    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(String(255))
    option_a : Mapped[str] = mapped_column(String(255))
    option_b : Mapped[str] = mapped_column(String(255))
    option_c : Mapped[str] = mapped_column(String(255))
    option_d : Mapped[str] = mapped_column(String(255))
    correct: Mapped[str] = mapped_column(String(255))

class UserStat(TimestampMixin, Base):
    __tablename__ = "user_stats"
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    fullname : Mapped[str] = mapped_column(String(255))
    score: Mapped[int] = mapped_column(Integer)
