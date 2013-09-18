from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.comments.models import Comment
from fluent_comments.moderation import moderate_model, comments_are_open, comments_are_moderated
from fluent_comments.models import get_comments_for_model, CommentsRelation


class Article(models.Model):
    title = models.CharField("Title", max_length=200)
    slug = models.SlugField("Slug", unique=True)
    content = models.TextField("Content")

    publication_date = models.DateTimeField("Publication date")
    enable_comments = models.BooleanField("Enable comments", default=True)

    # Optional reverse relation, allow ORM querying:
    comments_set = CommentsRelation()

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-details', kwargs={'slug': self.slug})

    # Optional, give direct access to moderation info via the model:
    comments = property(get_comments_for_model)
    comments_are_open = property(comments_are_open)


class CommentWithTitle(Comment):
    title = models.CharField(max_length=300)
