from django.contrib.auth.models import User

from core.models import Profile


def get_user(username):

    user = User.objects.get(username=username)
    return Profile.objects.get(user=user)
