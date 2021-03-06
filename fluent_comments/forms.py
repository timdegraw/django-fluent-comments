import importlib
from django.contrib.comments import CommentForm
from django.core.exceptions import ImproperlyConfigured
from fluent_comments import appsettings



if appsettings.USE_CUSTOM_COMMENTS:
    custom_comment_form_module = importlib.import_module(appsettings.CUSTOM_COMMENT_FORM_DIR)
    base_class = getattr(custom_comment_form_module, appsettings.CUSTOM_COMMENT_FORM_NAME)
elif appsettings.USE_THREADEDCOMMENTS:
    from threadedcomments.forms import ThreadedCommentForm as base_class
else:
    base_class = CommentForm


class FluentCommentForm(base_class):
    """
    The comment form, applies various settings.
    """
    def __init__(self, *args, **kwargs):
        super(FluentCommentForm, self).__init__(*args, **kwargs)
        # Remove fields from the form.
        # This has to be done in the constructor, because the ThreadedCommentForm
        # inserts the title field in the __init__, instead of the static form definition.
        for name in appsettings.FLUENT_COMMENTS_EXCLUDE_FIELDS:
            try:
                self.fields.pop(name)
            except KeyError:
                raise ImproperlyConfigured("Field name '{0}' in FLUENT_COMMENTS_EXCLUDE_FIELDS is invalid, it does not exist in the comment form.")


    def get_comment_create_data(self):
        # Fake form data for excluded fields, so there are no KeyError exceptions
        for name in appsettings.FLUENT_COMMENTS_EXCLUDE_FIELDS:
            self.cleaned_data[name] = ""

        return super(FluentCommentForm, self).get_comment_create_data()

