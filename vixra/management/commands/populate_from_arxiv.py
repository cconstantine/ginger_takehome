from django.core.management.base import BaseCommand, CommandError

from vixra.models import Article

class Command(BaseCommand):
  help = "Populate database from arXiv"

  def handle(self, *args, **options):
    Article.populate_from_arxiv()