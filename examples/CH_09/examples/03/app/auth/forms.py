from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError
from .. models import User, db_session_manager


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired(), Length(
            min=4,
            max=128,
            message="Email must be between 4 and 128 characters long"
        ), Email()],
        render_kw={"placeholder": " ", "tabindex": 1, "autofocus": True}
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(
            min=3,
            max=64,
            message="Password must be between 3 and 64 characters long"
        )],
        render_kw={"placeholder": " ", "tabindex": 2}
    )
    remember_me = BooleanField(
        " Keep me logged in",
        render_kw={"tabindex": 3}
    )
    login = SubmitField("Log In", render_kw={"tabindex": 4})
    cancel = SubmitField("Cancel", render_kw={"tabindex": 5})


class RegisterNewUserForm(FlaskForm):
    first_name = StringField(
        "First Name",
        validators=[DataRequired()],
        render_kw={"placeholder": " ", "tabindex": 1, "autofocus": True}
    )
    last_name = StringField(
        "Last Name",
        validators=[DataRequired()],
        render_kw={"placeholder": " ", "tabindex": 2}
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(), Length(
            min=4,
            max=128,
            message="Email must be between 4 and 128 characters long"
        ), Email()],
        render_kw={"placeholder": " ", "tabindex": 3}
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(
            min=3,
            max=64,
            message="Password must be between 3 and 64 characters long"
        ),
            EqualTo("confirm_password", message="Passwords must match")
        ],
        render_kw={"placeholder": " ", "tabindex": 4}
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), Length(
            min=3,
            max=64,
            message="Password must be between 3 and 64 characters long"
        )],
        render_kw={"placeholder": " ", "tabindex": 5}
    )
    create_new_user = SubmitField("Create New User", render_kw={"tabindex": 6})
    cancel = SubmitField("Cancel", render_kw={"tabindex": 7})

    def validate_email(self, field):
        with db_session_manager() as db_session:
            user = db_session.query(User).filter(User.email == field.data).one_or_none()
            if user is not None:
                raise ValidationError("Email already registered")
