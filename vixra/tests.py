from django.test import TestCase

# Create your tests here.
from vixra.models import Article, Author

import arxiv
import datetime

class AuthorTestCase(TestCase):

  #sanity check that django works
  def test_author_from_name(self):
    self.assertEquals(Author.objects.count(), 0)

    first_get_or_create, _ = Author.objects.get_or_create(name = "Robert Bob")
    
    self.assertEquals(Author.objects.count(), 1)

    second_get_or_create, _ = Author.objects.get_or_create(name = "Robert Bob")

    self.assertEquals(first_get_or_create.id, second_get_or_create.id)


class ArticleTestCase(TestCase):
  def test_article_from_arxiv_response_dict(self):
    self.assertEquals(Article.objects.count(), 0)
    self.assertEquals(Author.objects.count(), 0)

    # I don't like making a live call here, but I can't find a better way
    response = arxiv.query("cat:cs.AI", sort_by="submittedDate", sort_order="descending", max_results=1)[0]

    article, created = Article.from_arxiv_response(response)

    self.assertIsInstance(article, Article)
    self.assertTrue(created)
    self.assertEquals(Article.objects.count(), 1)

    self.assertGreater(Author.objects.count(), 0)
    self.assertEquals(article.authors.count(), Author.objects.count())

    article.refresh_from_db()

    self.assertRegex(article.guid, r'arXiv:.+')
    self.assertEquals(article.title, response['title'])
    self.assertEquals(article.summary, response['summary'])
    self.assertIsInstance(article.publish_date, datetime.datetime)

    article2, created = Article.from_arxiv_response(response)
    self.assertFalse(created)
    self.assertEquals(Article.objects.count(), 1)
    self.assertEquals(article.guid, article2.guid)


# TODO: Test views
