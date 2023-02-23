from contextlib import contextmanager
from enum import Flag, auto
from flask import current_app
from flask_bcrypt import (
    generate_password_hash,
    check_password_hash
)
from sqlalchemy import func
from . import db
from flask_login import UserMixin
from uuid import uuid4
from datetime import datetime, timezone
from itsdangerous import (
    URLSafeTimedSerializer,
    SignatureExpired,
    BadSignature
)
from time import time
import jwt


@contextmanager
def db_session_manager(session_close=True):
    """Creates a context manager to use to interact
    with the database session and assure closing
    the session at the end of the scope

    Yields:
        Session: The database session object to use
    """
    try:
        yield db.session
    except Exception:
        db.session.rollback()
        raise
    finally:
        if session_close:
            db.session.close()


def get_uuid():
    """Generate a shortened UUID4 value to use
    as the primary key for database records

    Returns:
        string: A shortened (no '-' characters) UUID4 value
    """
    return uuid4().hex


# the association table used the create the many-to-many relationship between
# the user and post tables
user_post = db.Table(
    "user_post",
    db.Column("user_uid", db.String, db.ForeignKey("user.user_uid")),
    db.Column("post_uid", db.String, db.ForeignKey("post.post_uid"))
)


class User(UserMixin, db.Model):
    """The User class to structure what
    a user looks like for the MyBlog application. This
    capitalizes on the flask_login UserMixin class for
    some default methods. The UserMixin class will be
    used more when users are persisted to a database.
    """
    __tablename__ = "user"
    user_uid = db.Column(db.String, primary_key=True, default=get_uuid)
    role_uid = db.Column(db.String, db.ForeignKey("role.role_uid"), index=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True, index=True)
    hashed_password = db.Column("password", db.String, nullable=False)
    posts = db.relationship("Post", backref=db.backref("user", lazy="joined"))
    posts_followed = db.relationship("Post", secondary=user_post, backref=db.backref("users_following", lazy="dynamic"))
    active = db.Column(db.Boolean, nullable=False, default=True)
    confirmed = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=timezone.utc))
    updated = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now(tz=timezone.utc),
        onupdate=datetime.now(tz=timezone.utc)
    )

    def get_id(self):
        return self.user_uid

    @property
    def password(self):
        raise AttributeError("user password can't be read")

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def confirmation_token(self):
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return serializer.dumps({"confirm": self.user_uid})

    def confirm_token(self, token):
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        with db_session_manager() as db_session:
            confirmation_link_timeout = current_app.config.get("CONFIRMATION_LINK_TIMEOUT")
            timeout = confirmation_link_timeout * 60 * 1000
            try:
                data = serializer.loads(token, max_age=timeout)
                if data.get("confirm") != self.user_uid:
                    return False
                self.confirmed = True
                db_session.add(self)
                return True
            except (SignatureExpired, BadSignature):
                return False

    def get_reset_token(self, timeout):
        timeout *= 60
        return jwt.encode(
            {
                "reset_password": self.user_uid,
                "exp": time() + timeout,
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )

    @staticmethod
    def verify_reset_token(token):
        user_uid = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )["reset_password"]
        return user_uid

    def can_view_posts(self):
        can_view = (self.role.permissions | Role.Permissions.REGISTERED).value
        return 0 <= can_view <= 1

    def __repr__(self):
        return f"""
        user_uid: {self.user_uid}
        name: {self.first_name} {self.last_name}
        email: {self.email}
        confirmed: {self.confirmed}
        active: {'True' if self.active else 'False'}
            role_uid: {self.role.role_uid}
            name: {self.role.name}
            description: {self.role.description}
            permissions: {self.role.permissions}
        created: {self.created}
        updated: {self.updated}
        """


class Role(db.Model):
    """The Role class which is essentially a lookup table
    used to contain the roles supported by the MyBlog
    application
    """
    class Permissions(Flag):
        """This internally defined class creates the
        permissions bitmasks. It's internal here
        just to contain it within the scope of the
        Role class

        Args:
            Flag (enum.Flag): The bitmask value of a permissions
        """
        REGISTERED = auto()
        EDITOR = auto()
        ADMINISTRATOR = auto()

    __tablename__ = "role"
    role_uid = db.Column(db.String, primary_key=True, default=get_uuid)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    raw_permissions = db.Column(db.Integer)
    users = db.relationship("User", backref=db.backref("role", lazy="joined"))
    active = db.Column(db.Boolean, nullable=False, default=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=timezone.utc))
    updated = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now(tz=timezone.utc),
        onupdate=datetime.now(tz=timezone.utc)
    )

    @property
    def permissions(self):
        return Role.Permissions(self.raw_permissions)

    @staticmethod
    def initialize_role_table():
        """This static method is used to initialize/update the role table
        based on the roles list defined below. This is useful as the role
        table is a read-only lookup table that needs data in it to
        start with.
        """
        roles = [
            {
                "name": "user",
                "description": "registered user permission",
                "raw_permissions": Role.Permissions.REGISTERED.value
            },
            {
                "name": "editor",
                "description": "user has ability to edit all content and comments",
                "raw_permissions": (Role.Permissions.REGISTERED | Role.Permissions.EDITOR).value
            },
            {
                "name": "admin",
                "description": "administrator user with access to all of the application",
                "raw_permissions": (
                    Role.Permissions.REGISTERED |
                    Role.Permissions.EDITOR |
                    Role.Permissions.ADMINISTRATOR
                ).value
            }
        ]
        with db_session_manager() as db_session:
            for r in roles:
                role = db_session.query(Role).filter(Role.name == r.get("name")).one_or_none()

                # is there no existing role by a given name?
                if role is None:
                    role = Role(
                        name=r.get("name"),
                        description=r.get("description"),
                        raw_permissions=r.get("raw_permissions")
                    )
                # otherwise, need to update existing role permissions
                else:
                    role.description = r.get("description")
                    role.raw_permissions = r.get("raw_permissions")

                db_session.add(role)
            db_session.commit()

    def __repr__(self):
        return f"""
        role_uid: {self.role_uid}
        name: {self.name}, description: {self.description}
        permissions: {self.permissions}
        active: {'True' if self.active else 'False'}
        created: {self.created}
        updated: {self.updated}
        """


def get_next_sort_key() -> int:
    """Generates an incrementing sort_key value from the database

    Raises:
        RuntimeError: If the query fails, raises an exception

    Returns:
        integer: The new max value sort_key to use
    """
    with db_session_manager(session_close=False) as db_session:
        retval = db_session.query(func.ifnull(func.max(Post.sort_key) + 1, 0)).scalar()
        if retval is None:
            raise RuntimeError("Failed to get new value for sort_key")
        return retval


class Post(db.Model):
    """The post class holds the main blog posts content and comments for the
    MyBlog application
    """
    __tablename__ = "post"
    post_uid = db.Column(db.String, primary_key=True, default=get_uuid)
    parent_uid = db.Column(db.String, db.ForeignKey("post.post_uid"), default=None)
    sort_key = db.Column(db.Integer, nullable=False, unique=True, default=get_next_sort_key)
    user_uid = db.Column(db.String, db.ForeignKey("user.user_uid"), nullable=False, index=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    children = db.relationship("Post", backref=db.backref("parent", remote_side=[post_uid], lazy="joined"))
    active = db.Column(db.Boolean, nullable=False, default=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=timezone.utc))
    updated = db.Column(db.DateTime, nullable=False, default=datetime.now(
        tz=timezone.utc), onupdate=datetime.now(tz=timezone.utc))

    def __repr__(self):
        return f"""
        post_uid: {self.post_uid}
        parent_uid: {self.parent_uid}
        sort_key: {self.sort_key}
        title: {self.title}
        content: {self.content}
        active: {'True' if self.active else 'False'}
        created: {self.created}
        updated: {self.updated}
        """
