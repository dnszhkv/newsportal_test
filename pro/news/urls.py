from django.urls import path
from django.contrib.auth.views import LoginView
# Импортирую представления
from .views import (PostList, PostDetail, PostSearch, NewCreate, NewUpdate, NewDelete, PostCategory,
                    subscribe_to_category, unsubscribe_from_category)
from django.views.decorators.cache import cache_page


urlpatterns = [
   # Вызываю метод as_view.
   path('', cache_page(60)(PostList.as_view()), name='post_list'),
   # pk — первичный ключ поста, который будет выводиться в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>/', cache_page(60*5)(PostDetail.as_view()), name='new'),
   path('search/', PostSearch.as_view(), name='search'),
   path('create/', NewCreate.as_view(), name='new_create'),
   path('<int:pk>/edit/', NewUpdate.as_view(), name='NE_edit'),
   path('<int:pk>/delete/', NewDelete.as_view(), name='NE_delete'),
   path('category/<int:pk>/', PostCategory.as_view(), name='category'),
   path('subscribe/<int:pk>/', subscribe_to_category, name='subscribe'),
   path('unsubscribe/<int:pk>/', unsubscribe_from_category, name='unsubscribe'),
]