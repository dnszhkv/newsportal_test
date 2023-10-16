from django.urls import path
# Импортирую представления
from .views import ArticleCreate, ArticleUpdate, ArticleDelete


urlpatterns = [
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]