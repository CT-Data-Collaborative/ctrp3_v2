from django.db.models import DateField
from markdownx.models import MarkdownxField

from .helpers import SingletonModel, MarkdownModel

class HomePage(SingletonModel, MarkdownModel):
    about = MarkdownxField()
    start = DateField(blank=True, null=True)
    end = DateField(blank=True, null=True)
