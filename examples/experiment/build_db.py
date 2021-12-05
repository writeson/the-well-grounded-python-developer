"""Create the database for the blogging platform
"""

import os
import pathlib
from datetime import datetime
from datetime import timezone
from uuid import uuid4

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import event
from sqlalchemy import DDL
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import UUIDType

load_dotenv()

# get rid of old database if it exists
db_path = pathlib.Path(__file__).parent / "data" / "blog.sqlite"
if db_path.exists():
    db_path.unlink()

# get going with SqlAlchemy
Base = declarative_base()
engine = create_engine(f"sqlite:///{db_path}", echo=True)
Session = sessionmaker(bind=engine)
session = Session()


print("Done")


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType(), unique=True, nullable=False, default=uuid4)
    fname = Column(String(30), nullable=False)
    lname = Column(String(30), nullable=False)
    email = Column(String(64), nullable=False)
    role_id = Column(Integer, ForeignKey("role.role_id"))
    role = relationship("Role")
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.utcnow)
    active = Column(Integer, nullable=False, default=1)

    def __repr__(self):
        return f"User: {self.fname} {self.lname}"


event.listen(
    User.__table__,
    "after_create",
    DDL("""
        CREATE TRIGGER user_updated_after_update AFTER UPDATE ON user
        BEGIN
            UPDATE user SET updated=CURRENT_TIMESTAMP WHERE user_id=NEW.user_id;
        END;
    """
    )
)


class Role(Base):
    __tablename__ = "role"
    role_id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType(), unique=True, nullable=False, default=uuid4)
    name = Column(String(20), unique=True, nullable=False)
    description = Column(String(128), unique=True, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.utcnow)
    active = Column(Integer, nullable=False, default=1)

    def __repr__(self):
        return f"Role: {self.name}"


event.listen(
    Role.__table__,
    "after_create",
    DDL("""
        CREATE TRIGGER role_updated_after_update AFTER UPDATE ON role
        BEGIN
            UPDATE role SET updated = CURRENT_TIMESTAMP WHERE role_id=NEW.role_id;
        END;
    """
    )
)

Base.metadata.create_all(engine)

# Create the various roles in the system
role_admin = Role(
    name="admin",
    description="The administration user, who can do essentially anything",
)
role_registered = Role(
    name="registered",
    description="The registered user, who can create, edit and delete their own posts, and comment on others posts",
)
role_unregistered = Role(
    name="unregistered",
    description="The unregistered user, who can create, edit and delete comments on others posts",
)
session.add(role_admin)
session.add(role_registered)
session.add(role_unregistered)
session.commit()

# Add some users
doug = User(
    fname="Doug",
    lname="Farrell",
    email="doug.farrell@gmail.com",
    role=role_admin
)

susan = User(
    fname="Susan",
    lname="Farrell",
    email="farrell.sk@gmail.com",
    role=role_registered
)

session.add(doug)
session.add(susan)
session.commit()

import time
time.sleep(10)

doug = session.query(User).get(1)

v = 1

doug.active = 0
session.commit()

v = 1

