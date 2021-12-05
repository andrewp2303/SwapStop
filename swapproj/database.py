from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///swapstop.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)
    db_session.commit()

# sql-alchemy

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hash = Column(String, nullable=False)

    def __init__(self, first_name=None, last_name=None, email=None, username=None, password=None, is_admin=False):
        self.username = username
        self.hash = hash

    def __repr__(self):
        return f'<User {self.id, self.username!r}>'

class Item(Base):
    __tablename__ = 'items'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    img = Column(LargeBinary)
    timestamp = Column(DateTime, nullable=False)
    sold = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    def __init__(self, name=None, description=None, img=None, timestamp=None, sold=None, user_id=None):
        self.name = name
        self.description = description
        self.img = img
        self.timestamp = timestamp
        self.sold = sold
        self.user_id = user_id

    def __repr__(self):
        return f'<User {self.id, self.name!r}>'

class Message(Base):
    __tablename__ = 'messages'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey(User.id), nullable=False)
    rec_id = Column(Integer, ForeignKey(User.id), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    text = Column(String, nullable=False)
    item_id = Column(Integer, ForeignKey(Item.id), nullable=False)
    traded_item_id = Column(Integer, ForeignKey(Item.id), nullable=False)

    def __init__(self, sender_id=None, rec_id=None, timestamp=None, text=None, item_id=None, traded_item_id=None):
        self.sender_id = sender_id
        self.rec_id = rec_id
        self.timestamp = timestamp
        self.text = text
        self.item_id = item_id
        self.traded_item_id = traded_item_id


    def __repr__(self):
        return f'<User {self.id, self.timestamp!r}>'

class Trade(Base):
    __tablename__ = 'trades'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    item1_id = Column(Integer, ForeignKey(Item.id), nullable=False)
    item2_id = Column(Integer, ForeignKey(Item.id), nullable=False)

    def __init__(self, item1_id, item2_id):
        self.item1_id = item1_id
        self.item2_id = item2_id

    def __repr__(self):
        return f'<User {self.item1_id, self.item2_id!r}>'