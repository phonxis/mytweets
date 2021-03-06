from django.contrib import admin
from .models import Tweet, HashTag
from user_profile.models import UserFollowers

# Register your models here.


class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_date')
    list_filter = ('user', )
    ordering = ('-created_date', )
    search_fields = ('text', )

admin.site.register(Tweet, TweetAdmin)
admin.site.register(HashTag)
admin.site.register(UserFollowers)