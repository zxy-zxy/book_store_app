from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy


from books.models import Author, Publisher, Book
from books.factory import AuthorFactory, PublisherFactory, BookFactory


class AuthorModelTest(TestCase):
    def test_create_author_successfully(self):
        author = AuthorFactory()
        self.assertEqual(Author.objects.count(), 1)

    def test_create_author_with_exists_name_raises_error(self):
        author = AuthorFactory()
        new_author = Author(first_name=author.first_name, last_name=author.last_name)
        with self.assertRaises(IntegrityError):
            new_author.save()


class PublisherModelTest(TestCase):
    def test_create_publisher_successful(self):
        publisher = PublisherFactory()
        self.assertEqual(Publisher.objects.count(), 1)

    def test_create_publisher_with_exists_name_raises_error(self):
        publisher = PublisherFactory()
        new_publisher = Publisher(name=publisher.name)
        with self.assertRaises(IntegrityError):
            new_publisher.save()


class BookModelTest(TestCase):
    def test_create_book_successfully(self):
        book = BookFactory()
        self.assertEqual(Book.objects.count(), 1)

    def test_create_book_with_same_isbn_raises_error(self):
        publisher = PublisherFactory()
        author = AuthorFactory()
        book = BookFactory()
        new_book = Book(
            author=author, publisher=publisher, isbn=book.isbn, title='Test book'
        )
        with self.assertRaises(IntegrityError):
            new_book.save()

    def test_create_book_with_invalid_isbn_raises_error(self):
        publisher = PublisherFactory()
        author = AuthorFactory()
        new_book = Book(
            author=author, publisher=publisher, isbn='ISBN', title='Test book'
        )
        with self.assertRaises(ValidationError):
            new_book.save()
            new_book.full_clean()

    def test_get_absolute_url(self):
        book = BookFactory()
        book_url = reverse_lazy('books:book_detail', kwargs={'isbn': book.isbn})
        self.assertEqual(book.get_absolute_url(), book_url)
