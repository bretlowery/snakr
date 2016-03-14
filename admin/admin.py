from django.contrib import admin
from snakr.models import LongURLs, ShortURLs

class LongURLsAdmin(admin.ModelAdmin):
    pass

class ShortURLsAdmin(admin.ModelAdmin):
    pass

admin.site.register(LongURLs, LongURLsAdmin)
admin.site.register(ShortURLs, ShortURLsAdmin)
