from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

from ..models import Blog


class BlogPostForm(FlaskForm):
    """
    Form for users to create new posts.
    """
    content = StringField(
        "Tweet",
        validators=[
            DataRequired(),
            Length(
                max=140,
                message="Tweet cannot contain more than 140 characters.")
        ])
    submit = SubmitField('Post')
