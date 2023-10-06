# Импортирую класс, который говорит о том, что в этом представлении будет выводиться список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post
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


# Создание новости
class NewCreate(CreateView):
    # Указываю разработанную форму,
    form_class = PostForm
    # модель постов
    model = Post
    # шаблон, в котором используется форма,
    template_name = 'new_edit.html'
    # и задаю страницу для перехода после выполнения операции
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NE'
        return super().form_valid(form)


# Изменение новости
class NewUpdate(UpdateView):
    form_class = PostForm
    model = Post
    success_url = reverse_lazy('post_list')

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
class NewDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

    def get_template_names(self):
        post = self.get_object()
        if post.type == 'NE':
            return ['new_delete.html']
        return super().get_template_names()


# Создание статьи
class ArticleCreate(CreateView):
    form_class = PostForm
    template_name = 'article_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        return super().form_valid(form)


# Редактирование статьи
class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    success_url = reverse_lazy('post_list')

    def get_template_names(self):
        post = self.get_object()
        if post.type == 'AR':
            return ['article_edit.html']
        return super().get_template_names()

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        return super().form_valid(form)


# Удаление статьи
class ArticleDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

    def get_template_names(self):
        post = self.get_object()
        if post.type == 'AR':
            return ['article_delete.html']
        return super().get_template_names()
