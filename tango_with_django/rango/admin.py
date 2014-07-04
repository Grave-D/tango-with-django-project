__author__ = 'user'

from django.contrib import admin
from rango.models import Category, Page, UserProfile


class PageAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'url')

admin.site.register(Page, PageAdmin)
admin.site.register(Category)
admin.site.register(UserProfile)