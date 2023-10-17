from django.urls import path
from django.contrib.auth.views import LoginView
# Импортирую представления
from .views import PostList, PostDetail, PostSearch, NewCreate, NewUpdate, NewDelete


urlpatterns = [
   # Вызываю метод as_view.
   path('', PostList.as_view(), name='post_list'),
   # pk — первичный ключ поста, который будет выводиться в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostDetail.as_view()),
   path('search/', PostSearch.as_view()),
   path('create/', NewCreate.as_view(), name='new_create'),
   path('<int:pk>/edit/', NewUpdate.as_view(), name='new_edit'),
   path('<int:pk>/delete/', NewDelete.as_view(), name='new_delete'),
]