from markdownx.models import MarkdownxField

from .helpers import SingletonModel, MarkdownModel

class HomePage(SingletonModel, MarkdownModel):
    about = MarkdownxField()
