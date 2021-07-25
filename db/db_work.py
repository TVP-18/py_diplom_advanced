import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import DATABASE_URL

Base = declarative_base()
engine = sq.create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


class UsersVk(Base):
    __tablename__ = 'users'

    id = sq.Column(sq.Integer, primary_key=True)
    settings = sq.Column(sq.String)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return f'{self.id}'


def exists_user(user_id):
    with Session() as session:
        result = session.query(UsersVk).filter(UsersVk.id == user_id)

    return False if result.first() is None else True


def add_user(user):
    with Session() as session:
        session.add(user)
        session.commit()


if __name__ == '__main__':
    print(exists_user(6))

