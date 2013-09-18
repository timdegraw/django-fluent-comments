from django.conf import settings
from django.contrib import admin
from django.contrib import comments
from django.contrib.admin.widgets import AdminTextInputWidget
from django.core.exceptions import ImproperlyConfigured
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from fluent_comments import appsettings


# Ensure the admin app is loaded,
# so the model is unregistered here, and not loaded twice.
if appsettings.USE_THREADEDCOMMENTS:
    # Avoid getting weird situations where both comment apps are loaded in the admin.
    if not hasattr(settings, 'COMMENTS_APP') or settings.COMMENTS_APP == 'comments':
        raise ImproperlyConfigured("To use 'threadedcomments', specify the COMMENTS_APP as well")

    from threadedcomments.admin import ThreadedCommentsAdmin as CommentsAdminBase
else:
    from django.contrib.comments.admin import CommentsAdmin as CommentsAdminBase
