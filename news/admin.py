from django.contrib import admin
from news.models import *
# Register your models here.

class GetNewsInfoMixin:
    def Comments(self, obj):
        return ', '.join(
            comment[:20] + '...' if len(comment) > 20 else comment # коментарий
            for comment in [c.comment_text for c in obj.comments.all()]
        )
    # get_news_comments.short_description = "Комментарии"

class NewsAdmin(GetNewsInfoMixin, admin.ModelAdmin):
    list_display = ['title','Comments']



admin.site.register(News,NewsAdmin)
admin.site.register(NewsComment)
admin.site.register(Tag)


































