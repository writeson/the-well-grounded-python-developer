from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_pagedown.fields import PageDownField
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(
            min=4,
            max=128
        )],
        render_kw={"placeholder": " ", "tabindex": 1, "autofocus": True}
    )
    content = PageDownField(
        "Content",
        validators=[DataRequired()],
        render_kw={"placeholder": " ", "tabindex": 2}
    )
    post_create = SubmitField(
        "Create Blog Post",
        render_kw={"tabindex": 3}
    )
    cancel = SubmitField("Cancel", render_kw={"tabindex": 4})


class PostUpdateForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(
            min=4,
            max=128
        )],
        render_kw={"placeholder": " ", "tabindex": 1}
    )
    content = PageDownField(
        "Content",
        validators=[DataRequired()],
        render_kw={"placeholder": " ", "tabindex": 2, "autofocus": True}
    )
    active_state = HiddenField("active_state")
    post_update = SubmitField(
        "Update Blog Post",
        render_kw={"tabindex": 3}
    )
    activate = SubmitField(
        "Activate",
        render_kw={"tabindex": 4}
    )
    deactivate = SubmitField(
        "Deactivate",
        render_kw={"tabindex": 5}
    )
    cancel = SubmitField(
        label="Cancel",
        render_kw={"tabindex": 6}
    )
