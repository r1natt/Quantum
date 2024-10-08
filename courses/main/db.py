from .models import engine, UsersTable
from sqlalchemy import insert, select
import hashlib 


class Users:
    def _md5_hash(string):
        return hashlib.md5(f"{email}+{password}".encode()).hexdigest()

    def is_user_in_db(self, email, password) -> bool:
        with engine.connect() as conn:
            stmt = (select(Users).
                    where(email, password)
                )
            return True if conn.execute(stmt).one() else False

    def get_user_hash(self, email, password) -> str:
        with engine.connect() as conn:
            stmt = (select(Users.hash_id).
                    where(email, password)
                )
            return conn.execute(stmt).one()[0]

    def insert_new_user(self, email, password) -> None:
        with engine.connect() as conn:
            stmt = (
                insert(Users.hash_id).
                    values(
                        email=email,
                        password=password,
                        hash_id=self._md5_hash(email + password)
                    )
                )
            conn.execute(stmt)
            conn.commit()