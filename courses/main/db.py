from .models import engine, UsersTable
from sqlalchemy import insert, select
import hashlib 


class Users:
    def _md5_hash(self, string):
        return hashlib.md5(string.encode()).hexdigest()

    def is_user_in_db(self, email, password) -> bool:
        with engine.connect() as conn:
            stmt = (select(UsersTable).
                    where(
                        UsersTable.email == email, 
                        UsersTable.password == password
                    )
                )
            return True if conn.execute(stmt).all() else False

    def get_user_hash(self, email, password) -> str:
        with engine.connect() as conn:
            stmt = (select(UsersTable.hash_id).
                    where(
                        UsersTable.email == email, 
                        UsersTable.password == password
                    )
                )
            return conn.execute(stmt).one()[0]

    def insert_new_user(self, email, password) -> None:
        with engine.connect() as conn:
            stmt = (
                insert(UsersTable).
                    values(
                        email=email,
                        password=password,
                        hash_id=self._md5_hash(email + password)
                    )
                )
            conn.execute(stmt)
            conn.commit()
