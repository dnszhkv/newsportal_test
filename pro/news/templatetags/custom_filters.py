from django import template
import re

register = template.Library()

CENSOR_WORDS = ['редиск']


# Регистрирую фильтр
@register.filter(name='censor')
def censor(text):
   # Прохожу по каждому слову в тексте
   words = text.split()
   censored_words = []

   for word in words:
      # Привожу слова к нижнему регистру для сравнения
      lowercase_word = word.lower()

      # Если основа слова есть в списке нежелательных слов, заменяю символами "*"
      if any(re.match(rf'\b{re.escape(word_base)}\w*\b', lowercase_word) for word_base in CENSOR_WORDS):
         censored_word = word[0] + '*' * len(word[1:])
         censored_words.append(censored_word)
      else:
         censored_words.append(word)

   # Собираю обратно текст с цензурированными словами
   censored_text = ' '.join(censored_words)

   return censored_text