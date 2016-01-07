from django.test import TestCase
from django.core.urlresolvers import reverse
# Create your tests here.
from rango.models import Category, Page

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

def add_page(title, url, views, slug):
    c = Category.objects.get(slug=slug)
    p = Page.objects.create(title=title, url=url, views=views, category=c)
    return p


class CategoryMethodTests(TestCase):

    def test_ensure_views_are_positive(self):
        """
        ensure_views_are_posivtive should results True for categories where views are zero or positive"""

        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        """
        slug_line_creation checks to make sure that when we add a category an appropriate slug line is created
        i.e. "Rando Category String" -> "rango-category-string"
        """
        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')


class IndexViewTests(TestCase):

    def test_index_view_with_no_categories(self):
        """
        If no questions exist, an anproriate message should be displayed.
        """

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])



    def test_index_view_with_categories(self):
        """
        If no questions exist, an appropirate message should be displayed.
        """

        add_cat('test', 1, 1)
        add_cat('temp', 1, 1)
        add_cat('tmp', 1, 1)
        add_cat('tmp test temp', 1, 1)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tmp test temp')

        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats, 4)

    def test_index_view_with_pages(self):

        add_cat('test', 1, 1)
        add_cat('another test', 2, 2)
        add_page('test_page', 'http://noname.com', 23, 'test')
        add_page('another_page_in_test_cat', 'http://abc.com', 2, 'test')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'noname')
        num_pages = len(response.context['pages'])
        num_cats = len(response.context['categories'])
        self.assertEqual(num_pages, 2)
        self.assertEqual(num_cats, 2)
        print type(response.context)


