from django.contrib.auth.models import User
from news.models import *


user1 = User.objects.create_user('Андрей', password='password1')
user2 = User.objects.create_user('Иван', password='password2')
user3 = User.objects.create_user('Наталья', password='password3')
user4 = User.objects.create_user('Степан', password='password4')


author1 = Author.objects.create(name=user1.username, user=user1)
author2 = Author.objects.create(name=user2.username, user=user2)


Category.objects.create(name='нейросети')
Category.objects.create(name='интересное')
Category.objects.create(name='наука')
Category.objects.create(name='познавательное')


article1 = Post.objects.create(author=author1, type='AR', title='Вспомнить всё: как амнезическое кино изгоняет, '
                                                                'отменяет и реставрирует историю',
                               text='Разговор о кризисе памяти столь же тривиален, как разговор о погоде. И тем не '
                                    'менее он не устаревает. Более того, становится предметом моды, шагнув с '
                                    'философских подмостков в поле кинематографа, из области теории в область '
                                    'общественных вкусов. Казалось бы, всё должно быть наоборот. «Катастрофическое '
                                    'сознание» и «клиповая реальность» как будто бы готовят нам нескончаемое забвение. '
                                    'И — благостное существование в бесконечном сегодня, без ощущения неполноты и '
                                    'виновности, даруемой историческим прошлым. Однако новая катастрофическая '
                                    'реальность всё настоятельнее вписывает человека в историю, ещё теснее связывая с '
                                    'прошлым. Перефразируя Диди-Юбермана, можно сказать, что человек есть то, в чём он '
                                    'больше всего нуждается. А значит, не по причине одной лишь моды и глобалистского '
                                    'стереотипа появляются фильмы об амнезии. У этой «утраты памяти» есть своя '
                                    'предыстория, свой анамнез недугов вроде «компьютерных революций», «фрагментации '
                                    'зрения» и «эстетики клипа». Конечно, и до всяких компьютерных революций амнезия '
                                    'была излюбленной темой кинематографа. О беспамятстве мечтали сюрреалисты, им '
                                    'грезили герои американского нуара или сновидцы вроде Рауля Руиса. На языке '
                                    'забвения говорили о разном: в 1920-е — об идеальной нестойкости мира; в 1960-е — '
                                    'об исторической травме Алжира, Хиросимы и Холокоста. Да, амнезия всегда '
                                    'оставалась популярным сюжетом, однако в разное время она вызывала к жизни свой '
                                    'визуальный контекст. Именно об этой разности контекстов и пойдет речь. Я '
                                    'попытаюсь отделить амнезию вчерашнюю от амнезии сегодняшней. В первом случае '
                                    'вырисовывается тенденция ощущения виновности. Во втором — поиски вины. А между '
                                    'тем виновность есть чувство, с которого история начинается.')

article2 = Post.objects.create(author=author2, type='AR', title='Клинический случай ахалазии пищевода',
                               text='Изучение ахалазии кардии остается актуальным вопросом, поскольку в настоящее '
                                    'время до сих пор однозначно нельзя сказать об этиологии данного заболевания. '
                                    'Ахалазия кардии является редким заболеванием, в основе которого лежит первичное '
                                    'расстройство моторики пищевода. Она характеризуется снижением перистальтики '
                                    'пищевода и неполной релаксацией зачастую тонически сокращенного нижнего '
                                    'пищеводного сфинктера в ответ на акт глотания [1]. В настоящее время '
                                    'рассматривают три основные гипотезы: генетическую, аутоиммунную и инфекционную. '
                                    'Цель: рассмотреть особенности течения заболевания ахалазии кардии на основе '
                                    'клинического случая пациента 29 лет.')

news1 = Post.objects.create(author=author1, type='NE', title='Netflix закончил рассылку DVD-дисков',
                            text='Стриминговый гигант Netflix разослал последние прокатные DVD-диски для жителей США. '
                                 'Услугой пользовались с 1998 года. «29 сентября 2023 года Netflix отправит свой '
                                 'последний DVD. Но красный конверт останется непреходящим символом нашей любви к '
                                 'развлечениям», — заявили в пресс-службе Netflix. После 29 сентября компания не '
                                 'будут взимать плату за невозвращённые диски. Также в конце года будет закрыт сервис '
                                 'DVD.com из-за сокращений в бизнесе. Всего с 1998 года Netflix разослал более '
                                 '5,2 млрд дисков DVD и Blu-ray. Первым доставленным фильмом был «Битлджус» '
                                 'Тима Бёртона.')


category_film = Category.objects.get(name='кино')
category_inter = Category.objects.get(name='интересное')
category_science = Category.objects.get(name='наука')
category_smart = Category.objects.get(name='познавательное')

PostCategory.objects.create(post=article1, category=category_film)
PostCategory.objects.create(post=article1, category=category_inter)
PostCategory.objects.create(post=article2, category=category_science)
PostCategory.objects.create(post=article2, category=category_smart)
PostCategory.objects.create(post=news1, category=category_film)


comment1 = Comment.objects.create(post=article1, user=user3, text='Интересная статья')
comment2 = Comment.objects.create(post=article2, user=user1, text='Статье не хватает новизны')
comment3 = Comment.objects.create(post=news1, user=user2, text='Конец эпохи')
comment4 = Comment.objects.create(post=article1, user=user4, text='Нетривиальная тема')


article1.like()
article2.dislike()
comment1.like()
comment2.like()
comment3.dislike()
comment4.like()


author1.update_rating()
author2.update_rating()


# best_author = Author.objects.order_by('-rating').first()
# print(f'Лучший пользователь: {best_author.user.username}, рейтинг: {best_author.rating}')
Author.objects.order_by('-rating').values('user__username', 'rating').first()


best_article = Post.objects.filter(type='AR').order_by('-rating').first()
print(f'Дата добавления: {best_article.time_in}')
print(f'Автор: {best_article.author.user.username}')
print(f'Рейтинг: {best_article.rating}')
print(f'Заголовок: {best_article.title}')
print(f'Превью: {best_article.preview()}')


comments_to_best_article = Comment.objects.filter(post=best_article)
for comment in comments_to_best_article:
    print(f'Дата: {comment.time_in}')
    print(f'Пользователь: {comment.user.username}')
    print(f'Рейтинг: {comment.rating}')
    print(f'Текст: {comment.text}')
