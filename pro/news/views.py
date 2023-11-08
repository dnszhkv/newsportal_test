# Импортирую класс, который говорит о том, что в этом представлении будет выводиться список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, resolve
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.conf import settings
from django.core.cache import cache

from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    # Указываю модель, объекты которой буду выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = ['-time_in']  # Устанавливаю сортировку от новых записей к ранним
    # Имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны объекты
    template_name = 'news.html'
    # Имя списка, в котором будут лежать все объекты.
    # Указывается, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10  # задаю количество записей на странице


# Создаю класс для поисковой страницы, наследуясь от основной
class PostSearch(PostList):
    # Переопределяю шаблон
    template_name = 'search.html'
    # Определяю функцию получения списка постов
    def get_queryset(self):
        # Получаю обычный запрос
        queryset = super().get_queryset()
        # Использую свой класс фильтрации. Сохраняю фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаю из функции отфильтрованный список постов
        return self.filterset.qs

    # Метод get_context_data позволяет изменить набор данных, который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляю в контекст объект фильтрации.
        context['filterset'] = self.filterset
        # Проверяю, если параметры фильтрации пусты - ставлю флаг пустого фильтра
        context['empty_filter'] = not any(self.filterset.form.cleaned_data.values())
        return context


class PostDetail(DetailView):
    # Модель та же, но информации выдаётся по отдельному посту
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class PostCategory(ListView):
    model = Post
    ordering = ['-time_in']
    template_name = 'category.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        category = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.get(id=self.id)
        subscribed = category.subscribers.filter(email=user.email)
        if not subscribed:
            context['category'] = category

        return context


@login_required
def subscribe_to_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        html = render_to_string(
            'mail/subscribed.html',
            {
                'category': category,
                'user': user,
            }
        )

        msg = EmailMultiAlternatives(
            subject='News Portal Ultimate! Подписка на категорию',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email, ],
        )
        msg.attach_alternative(html, "text/html")

        try:
            msg.send()
        except Exception as e:
            print(e)
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('account_info')


@login_required
def unsubscribe_from_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
        return redirect('account_info')


# Создание новости
class NewCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    # Указываю разработанную форму,
    form_class = PostForm
    # модель постов
    model = Post
    # шаблон, в котором используется форма,
    template_name = 'new_edit.html'
    # и задаю страницу для перехода после выполнения операции
    success_url = reverse_lazy('post_list')
    # добавляю проверку прав доступа
    permission_required = 'news.add_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NE'
        post.author = Author.objects.get(user=self.request.user)
        post.save()
        return super().form_valid(form)


# Изменение новости
class NewUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    success_url = reverse_lazy('post_list')
    permission_required = 'news.change_post'

    def get_template_names(self):
        post = self.get_object()
        if post.type == 'NE':
            return ['new_edit.html']
        return super().get_template_names()

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NE'
        return super().form_valid(form)


# Удаление новости
class NewDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    permission_required = 'news.delete_post'

    def get_template_names(self):
        post = self.get_object()
        if post.type == 'NE':
            return ['new_delete.html']
        return super().get_template_names()


# Создание статьи
class ArticleCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'article_edit.html'
    success_url = reverse_lazy('post_list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        post.author = Author.objects.get(user=self.request.user)
        post.save()
        # Сохранение статьи в кеш
        cache_key = f'article_{post.id}'  # Уникальный ключ для кеширования
        cache.set(cache_key, post)  # Сохранение статью в кеш
        return super().form_valid(form)


# Редактирование статьи
class ArticleUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    success_url = reverse_lazy('post_list')
    permission_required = 'news.change_post'

    def get_template_names(self):
        post = self.get_object()
        if post.type == 'AR':
            return ['article_edit.html']
        return super().get_template_names()

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        return super().form_valid(form)

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if post.type == 'AR':
            # Попытка получения статью из кеша
            cache_key = f'article_{post.id}'
            cached_post = cache.get(cache_key)
            if cached_post is not None:
                return cached_post
        return post


# Удаление статьи
class ArticleDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    permission_required = 'news.delete_post'

    def get_template_names(self):
        post = self.get_object()
        if post.type == 'AR':
            return ['article_delete.html']
        return super().get_template_names()

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if post.type == 'AR':
            # Удаление статью из кеша
            cache_key = f'article_{post.id}'
            cache.delete(cache_key)
        return super().delete(request, *args, **kwargs)
