from django.contrib import admin
from . models import feedbacks, wish, democratic, account, game, analyzedFeedbacks


# Register your models here.
admin.site.register(feedbacks)
admin.site.register(wish)
admin.site.register(democratic)
admin.site.register(account)
admin.site.register(game)
admin.site.register(analyzedFeedbacks)
