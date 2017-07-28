from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import HomePage

admin.site.register(HomePage, MarkdownxModelAdmin)
