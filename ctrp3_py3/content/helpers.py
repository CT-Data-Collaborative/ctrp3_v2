from django.db import models

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

class SingletonModel(models.Model):
    """Singleton Django Model
    Ensures there's always only one entry in the database, and can fix the
    table (by deleting extra entries) even if added via another mechanism.
    Also has a static load() method which always returns the object - from
    the database if possible, or a new empty (default) instance if the
    database is still empty. If your instance has sane defaults (recommended),
    you can use it immediately without worrying if it was saved to the
    database or not.
    Useful for things like system-wide user-editable settings.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Save object to the database. Removes all other entries if there
        are any.
        """
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Load object from the database. Failing that, create a new empty
        (default) instance of the object and return it (without saving it
        to the database).
        """

        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

class MarkdownModel(models.Model):
    """Abstract model for dynamically rendering markdown field as html

    Use a little bit of getattr magic to allow pseudo-dynamic transpilation of markdown fields to html.
    The primary use case is to allow for easy rendering of MarkdownXFields in templates without having
    to resort to template tags or filters.

    A model with a MarkdownxField could be rendered in a standard, function-based view by appending
    `__markdownify` to the field name.

    For example, here is a sample model:

    class HomePage(SingletonModel, MarkdownModel):
        about = MarkdownxField()

    A view using this model could be as follows:

    def home_page(request):
        home_page_content = HomePage.load()
        context = {
            'about': home_page_content.about__markdownify
        }
        return render(request, 'content/home.html', context)

    Appending `__markdownify` to a non-MarkdownX field will not trigger the rendering and will result in
    the model.Model getattr method being called on the field name being passed in.
    """

    class Meta:
        abstract = True

    # def __getattr__(self, item):
    #     base_item_name, cmd = item.split('__')
    #     if cmd == 'markdownify' and type(self._meta.get_field(base_item_name)) == MarkdownxField:
    #         return markdownify(self._meta.get_field(base_item_name).value_from_object(self))
    #     else:
    #         return models.Model.__getattribute__(self, item)
