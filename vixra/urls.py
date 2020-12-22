from django.urls import path

from . import views
app_name='vixra'
urlpatterns = [
  path('', views.index, name="index"),

  path('articles', views.article_index, name='article_index'),
  path('article/<guid>', views.article_show, name='article_show'),

  path('authors', views.author_index, name='authors_index'),
  path('author/<int:id>', views.author_show, name='author_show')
]