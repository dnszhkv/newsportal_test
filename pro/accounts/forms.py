from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


# Создаю форму для автоматического добавления
# зарегистрированных пользователей в группу 'common'
class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
