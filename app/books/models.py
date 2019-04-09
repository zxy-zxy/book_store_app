from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.urls import reverse

from .managers import BooksManager


class Author(models.Model):
    first_name = models.CharField(_('First name'), max_length=64)
    last_name = models.CharField(_('Last name'), max_length=64)
    date_of_birth = models.DateField(_('Date of birth'), blank=True, null=True)

    class Meta:
        unique_together = (('first_name', 'last_name'),)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('books:author_detail', kwargs={'pk': self.pk})


class Publisher(models.Model):
    name = models.CharField(_('Name'), unique=True, max_length=64)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('books:publisher_detail', kwargs={'pk': self.pk})


class Book(models.Model):
    isbn = models.CharField(
        _('ISBN'),
        max_length=13,
        unique=True,
        validators=[
            RegexValidator('^[\d-]+$', message='Only digits and hyphen are allowed.')
        ],
    )
    title = models.CharField(_('Title'), max_length=128)
    publisher = models.ForeignKey(
        'books.Publisher', on_delete=models.CASCADE, related_name='books'
    )
    author = models.ForeignKey(
        'books.Author', on_delete=models.CASCADE, related_name='books'
    )
    pages = models.IntegerField(_('Pages'), default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    objects = BooksManager()

    def __str__(self):
        return f'{self.title}, ISBN: {self.isbn} by {self.author}'

    def get_absolute_url(self):
        return reverse('books:book_detail', kwargs={'isbn': self.isbn})
