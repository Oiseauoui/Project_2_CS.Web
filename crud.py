# crud.py
from sqlalchemy.orm import Session
import models
import schemas
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    # Получаем пользователя по ид
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    # Получаем пользователя по имени
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    # Создаем пользователя, хешируем пароль, сохраняем в базу
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    # Получаем список пользователей
    return db.query(models.User).offset(skip).limit(limit).all()


def verify_password(plain_password, hashed_password):
    # Проверка на правильность пароля
    return pwd_context.verify(plain_password, hashed_password)


# Iuliia 18.02.24
def create_photo(db: Session, filename: str):
    # Створити новий запис про фотографію в базі даних
    photo = models.Photo(filename=filename)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo

# Iuliia 18.02.24
def delete_photo(db: Session, photo_id: int):
    # Видалення фотографії з бази даних за її ідентифікатором
    db.query(models.Photo).filter(models.Photo.id == photo_id).delete()
    db.commit()

# Iuliia 18.02.24
def update_photo(db: Session, photo_id: int, photo_data: dict):
    # Оновлення інформації про фотографію в базі даних
    db.query(models.Photo).filter(models.Photo.id == photo_id).update(photo_data)
    db.commit()

# Iuliia 18.02.24
def get_photo(db: Session, photo_id: int):
    # Отримання фотографії з бази даних за її ідентифікатором
    return db.query(models.Photo).filter(models.Photo.id == photo_id).first()
