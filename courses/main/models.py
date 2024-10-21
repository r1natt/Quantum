from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.utils import timezone


# class Users(AbstractBaseUser):
#     objects = UserManager()

#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#     )
#     password = models.CharField(max_length=30)
#     hash_id = models.CharField(max_length=32)

#     username = models.CharField(max_length=30)
#     date_joined = models.DateTimeField(default=timezone.now)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []


# from django_sorcery.db import databases

# db = databases.get("default")

# from sqlalchemy import String, create_engine
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# engine = create_engine(
#     f"postgresql+psycopg2://quantum:admin@localhost:5432/quantum", 
#     pool_size=10, 
#     max_overflow=20, 
#     pool_pre_ping=True
# )

# class Base(DeclarativeBase):
#     pass

# class UsersTable(Base):
#     __tablename__ = "users"

#     id: Mapped[int] = mapped_column(primary_key=True)

#     email: Mapped[str] = mapped_column(String(30))
#     password: Mapped[str] = mapped_column(String(30))
#     hash_id: Mapped[str] = mapped_column(String(32))

# Base.metadata.create_all(engine)

# class Users(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     email = db.Column(db.String(length=30))
#     password = db.Column(db.String(length=30))
#     hash_id = db.Column(db.String(length=30))
