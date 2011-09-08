from django.contrib import admin

from news.models import NewsItem



class NewsItemAdmin(admin.ModelAdmin):

    class Media:
        js = ('js/tiny_mce/tiny_mce.js',
              'ins_flatpages/admin/js/textareas.js',)



admin.site.register(NewsItem, NewsItemAdmin)
