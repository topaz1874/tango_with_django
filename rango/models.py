from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.views < 0:
            self.views = 0
        super(Category, self).save(*args, **kwargs)


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


class UserProfile(models.Model):
    # This line is required.Links UserProfile to a User Model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username


class PublishedArticlesManager(models.Manager):
    """define a custom model manager, which is a queryset that only
    returns the published articles."""

    def get_query_set(self):
        return super(PublishedArticlesManager, self).get_query_set(
            is_published=True)


class Article(models.Model):

    title = models.CharField(max_length=100)
    text = models.TextField(help_text="Formatted using ReST")
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User)
    is_published = models.BooleanField(default=False, verbose_name="Publish?")
    created_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager() # default model manager 
    # article = models.Manger()
    published = PublishedArticlesManager()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('wiki_article_detail', (), {'slug': self.slug})


class Edit(models.Model):

    article = models.ForeignKey(Article)
    editor = models.ForeignKey(User)
    edited_on = models.DateTimeField(auto_now_add=True)
    summary = models.CharField(max_length=100)

    class Meta:
        ordering = ['-edited_on']

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(
            self.summary, self.editor, self.edited_on)

    @models.permalink
    def get_absolute_url(self):
        return ('wiki_edit_detail', self.id)
