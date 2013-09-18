"""
API for :ref:`custom-comment-app-api`
"""
import importlib
from django.contrib.comments import Comment
from fluent_comments import appsettings
from fluent_comments.forms import FluentCommentForm


# following PEP 386
__version__ = "1.0a1"


if appsettings.USE_CUSTOM_COMMENTS:
    custom_comment_model_module = importlib.import_module(appsettings.CUSTOM_COMMENT_MODEL_DIR)
elif appsettings.USE_THREADEDCOMMENTS:
    # Extend the API provided by django-threadedcomments,
    # in case this app uses more hooks of Django's custom comment app API.
    from threadedcomments import *


def get_model():
    """
    Return the model to use for commenting.
    """

    if appsettings.USE_CUSTOM_COMMENTS:
        return getattr(custom_comment_model_module, appsettings.CUSTOM_COMMENT_MODEL_NAME)
    elif appsettings.USE_THREADEDCOMMENTS:
        return ThreadedComment
    else:
        return Comment


def get_form():
    """
    Return the form to use for commenting.
    """
    return FluentCommentForm
