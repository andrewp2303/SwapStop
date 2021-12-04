from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///exploration.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import explorationproj.models
    Base.metadata.create_all(bind=engine)
    db_session.commit()

# sql-alchemy

# users db
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False) # this isn't great might rethink this

    def __init__(self, first_name=None, last_name=None, email=None, username=None, password=None, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return f'<User {self.id, self.username!r}>'

# clubs db
class Club(Base):
    __tablename__ = 'clubs'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, unique=True, nullable=False)
    membership_process = Column(String, nullable=False)
    size = Column(String, nullable=False)
    is_accepting_members = Column(Boolean, default=True)
    recruiting_cycle = Column(String, nullable=False)
    time_commitment = Column(String, nullable=False)

    def __init__(self, title=None, description=None, membership_process=None, size=None, is_accepting_members=None, recruiting_cycle=False, time_commitment=None):
        self.title = title
        self.description = description
        self.membership_process = membership_process
        self.size = size
        self.is_accepting_members = is_accepting_members
        self.recruiting_cycle = recruiting_cycle
        self.time_commitment = time_commitment

    def __repr__(self):
        return f'<User {self.id, self.title!r}>'

# events db
class Event(Base):
    __tablename__ = 'events'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, unique=True, nullable=False)

    def __init__(self, datetime=None, title=None, description=None):
        self.datetime = datetime
        self.title = title
        self.description = description

    def __repr__(self):
        return f'<User {self.id, self.title!r}>'

# tags db
class Tag(Base):
    __tablename__ = 'tags'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return f'<User {self.id, self.name!r}>'
    
# club leaders db (users <> clubs)
class ClubLeader(Base):
    __tablename__ = 'club_leaders'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    club_id = Column(Integer, ForeignKey(Club.id), nullable=False)

    user = relationship('User', foreign_keys='ClubLeader.user_id')
    club = relationship('Club', foreign_keys='ClubLeader.club_id')

    def __init__(self, user_id=None, club_id=None):
        self.user_id = user_id
        self.club_id = club_id

    def __repr__(self):
        return f'<User {self.id, self.user_id, self.club_id!r}>'

# calendars db (users <> events)
class Calendar(Base):
    __tablename__ = 'calendars'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    event_id = Column(Integer, ForeignKey(Event.id), nullable=False)

    user = relationship('User', foreign_keys='Calendar.user_id')
    event = relationship('Event', foreign_keys='Calendar.event_id')

    def __init__(self, user_id=None, event_id=None):
        self.user_id = user_id
        self.event_id = event_id

    def __repr__(self):
        return f'<User {self.id, self.user_id, self.event_id!r}>'

# club tags db (clubs <> tags)
class ClubTag(Base):
    __tablename__ = 'club_tags'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    club_id = Column(Integer, ForeignKey(Club.id), nullable=False)
    tag_id = Column(Integer, ForeignKey(Tag.id), nullable=False)

    club = relationship('Club', foreign_keys='ClubTag.club_id')
    tag = relationship('Tag', foreign_keys='ClubTag.tag_id')

    def __init__(self, club_id=None, tag_id=None):
        self.club_id = club_id
        self.tag_id = tag_id

    def __repr__(self):
        return f'<User {self.id, self.club_id, self.tag_id!r}>'

# signups db (users <> clubs)
class Signup(Base):
    __tablename__ = 'signups'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    club_id = Column(Integer, ForeignKey(Club.id), nullable=False)

    user = relationship('User', foreign_keys='Signup.user_id')
    club = relationship('Club', foreign_keys='Signup.club_id')

    def __init__(self, user_id=None, club_id=None):
        self.user_id = user_id
        self.club_id = club_id

    def __repr__(self):
        return f'<User {self.id, self.user_id, self.club_id!r}>'

# club events db (clubs <> events)
class ClubEvent(Base):
    __tablename__ = 'club_events'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    club_id = Column(Integer, ForeignKey(Club.id), nullable=False)
    event_id = Column(Integer, ForeignKey(Event.id), nullable=False)

    club = relationship('Club', foreign_keys='ClubEvent.club_id')
    event = relationship('Event', foreign_keys='ClubEvent.event_id')

    def __init__(self, club_id=None, event_id=None):
        self.club_id = club_id
        self.event_id = event_id

    def __repr__(self):
        return f'<User {self.id, self.club_id, self.event_id!r}>'