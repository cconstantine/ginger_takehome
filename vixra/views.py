from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse

from .models import Article, Author

def index(request):
  return render(request, 'index.html')

# TODO: paginate
def article_index(request):
  articles = Article.objects.all()
  return render(request, 'articles/index.html', {"articles": articles})

def article_show(request, guid):
  article = get_object_or_404(Article, guid=guid)
  authors = article.authors.all() #TODO: sort correctly
  return render(request, 'articles/show.html', {"article": article, "authors": authors})

# TODO: paginate
def author_index(request):
  authors = Author.objects.all()
  #TODO: calculate article counts for all authors in one query
  return render(request, 'author/index.html', {"authors": authors})

def author_show(request, id):
  author = get_object_or_404(Author, id=id)
  articles = author.article_set.all()
  return render(request, 'author/show.html', {"author": author, 'articles': articles})