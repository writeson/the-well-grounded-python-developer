import re
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from flask_pagedown.fields import PageDownField
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired, Length
import bleach


def remove_html_and_script_tags(input_string: str) -> str:
    """Removes the html and script tags from the input
    string and returns the results

    Args:
        input_string (str): string provided by user in form

    Returns:
        str: the input string cleaned of html and script tags
    """
    return bleach.clean(input_string) if input_string is not None else input_string


class PostForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(
            min=4,
            max=128
        )],
        filters=(remove_html_and_script_tags,),
        render_kw={"placeholder": " ", "tabindex": 1, "autofocus": True}
    )
    content = PageDownField(
        "Content",
        validators=[DataRequired()],
        filters=(remove_html_and_script_tags,),
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
        filters=(remove_html_and_script_tags,),
        render_kw={"placeholder": " ", "tabindex": 1}
    )
    content = PageDownField(
        "Content",
        validators=[DataRequired()],
        filters=(remove_html_and_script_tags,),
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


class PostCommentForm(FlaskForm):
    parent_post_uid = HiddenField("parent_post_uid")
    comment = TextAreaField(
        "Comment",
        validators=[DataRequired()],
        filters=(remove_html_and_script_tags,),
        render_kw={"placeholder": " "}
    )
    create_comment = SubmitField(
        "Create",
    )
