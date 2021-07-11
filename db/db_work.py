import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from settings import DATABASE_URL

Base = declarative_base()

engine = sq.create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)


class UsersVk(Base):
    __tablename__ = 'users'

    id = sq.Column(sq.Integer, primary_key=True)
    settings = sq.Column(sq.String)


if __name__ == '__main__':
    # pass
    session = Session()
    cur_user = UsersVk(id=111, settings='dfsdfs')

    session.add(cur_user)
    session.commit()

