from django.contrib import admin
from .models import Category, Post


# Функция обнуления рейтинга постов
def nullify_rating(modeladmin, request, queryset):
    queryset.update(rating=0)
nullify_rating.short_description = 'Обнулить рейтинги'


# Создаю класс для представления постов в админке
class PostAdmin(admin.ModelAdmin):
    # список или кортеж со всеми полями, отображаемыми в таблице с постами
    list_display = ('title', 'author', 'time_in', 'type', 'rating')
    list_filter = ('author', 'rating', 'type')  # фильтры по полям
    actions = [nullify_rating]  # добавляю функцию


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
