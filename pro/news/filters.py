from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter
from .models import Author
from django import forms


# Создаю свой набор фильтров для поиска постов по критериям
class PostFilter(FilterSet):
    # по названию
    post = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название'
    )
    # по автору
    author = ModelChoiceFilter(
        field_name='author__name',
        queryset=Author.objects.all(),
        label='Автор'
    )
    # позже указываемой даты
    time_in__gte = DateFilter(
        field_name='time_in',
        lookup_expr='gt',
        label='Опубликовано после:',
        widget=forms.widgets.DateInput(attrs={'type': 'date'})
    )
