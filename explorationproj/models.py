# from sqlalchemy import Column, Integer, String, Boolean
# from explorationproj.database import Base

# class User(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True)
#     first_name = Column(String, nullable=False)
#     last_name = Column(String, nullable=False)
#     email = Column(String, unique=True, nullable=False)
#     username = Column(String, unique=True, nullable=False)
#     password = Column(String, nullable=False)
#     is_admin = Column(Boolean, default=False) # this isn't great might rethink this

#     def __init__(self, first_name=None, last_name=None, email=None, username=None, password=None, is_admin=False):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.email = email
#         self.username = username
#         self.password = password
#         self.is_admin = is_admin

#     def __repr__(self):
#         return f'<User {self.name!r}>'

