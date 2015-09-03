import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mytweets.settings")
from user_profile.models import User, UserFollowers

print(User.objects.all())
print(UserFollowers.objects.all())