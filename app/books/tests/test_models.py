from django.test import TestCase
from django.db.utils import IntegrityError

from books.models import Author, Publisher, Book
from books.factory import AuthorFactory


class AuthorModelTest(TestCase):
    def test_create_author_successful(self):
        author = AuthorFactory()
        self.assertEqual(Author.objects.count(), 1)

    def test_create_author_with_exists_name_raises_error(self):
        author = AuthorFactory()
        new_author = Author(first_name=author.first_name, last_name=author.last_name)
        with self.assertRaises(IntegrityError):
            new_author.save()


class PublisherModelTest(TestCase):
    pass
