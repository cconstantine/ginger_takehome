from django.db import models
from django.utils import timezone
import re
import datetime
import arxiv

class Article(models.Model):
  title = models.CharField(max_length=1000)
  summary = models.TextField()
  guid = models.CharField(max_length=200, unique=True)

  publish_date = models.DateTimeField('')
  authors = models.ManyToManyField('Author')

  @staticmethod
  def from_arxiv_response(obj):
    if obj['guidislink']:
      #extract arXiv id from link
      #  Ref: https://arxiv.org/help/arxiv_identifier
      raw_id = re.search(r'.*?([^/]+)$', obj['id']).group(1)
      guid = "arXiv:{guid}".format(guid=raw_id)
    else:
      # I don't know if this will ever happen, maybe an exception woud be better?
      guid = obj['id']

    article, created = Article.objects.get_or_create(
      guid = guid,
      defaults={
        'title': obj['title'],
        'summary': obj['summary'],
        'publish_date': obj['published']
        }
      )

    for author_name in obj['authors']:
      author, _ = Author.objects.get_or_create(name=author_name)
      article.authors.add(author)

    return article, created

  # Assumes papers are immutable
  # TODO: This method needs some work;
  #  * The query is hardcoded
  #  * It is not covered in test
  #  * The query gives wildly different results each run
  @staticmethod
  def populate_from_arxiv():
    three_months_ago = timezone.now() -  datetime.timedelta(days=30*3)

    num_created = 0
    print("Getting arXiv articles", end='')
    results = arxiv.query(query="cat:cs.LG OR all:psychiatry OR all:therapy", sort_by="submittedDate", sort_order="descending", iterative=True, max_chunk_results=10)

    for result in results():
      article, _ = Article.from_arxiv_response(result)
      article.refresh_from_db()
      if article.publish_date < three_months_ago:
        break
      print(".", end='')

      num_created += 1
    print("\nFinished {0}".format(num_created))

class Author(models.Model):
  name = models.CharField(max_length=1000, unique=True)
