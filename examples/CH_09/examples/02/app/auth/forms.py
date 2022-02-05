from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Length, Email


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
