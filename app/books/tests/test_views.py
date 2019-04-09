from django.forms.models import model_to_dict
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from books.factory import BookFactory, PublisherFactory, AuthorFactory
from books.models import Book


class BooksListViewTest(TestCase):
    def setUp(self):
        BookFactory.create_batch(10)

    def test_book_list_renders_correct_html(self):
        response = self.client.get(reverse('books:book_list'))
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_home_page_renders_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_list_contains_create_new_book_url(self):
        respone = self.client.get('/')
        create_new_book_url = reverse('books:book_create')
        self.assertContains(respone, create_new_book_url)

    def test_book_list_contains_book(self):
        book = Book.objects.first()
        response = self.client.get('/')
        self.assertContains(response, book.title)


class BookDetailViewTest(TestCase):
    def setUp(self):
        self.book = BookFactory()

    def test_book_detail_page_contains_book_details(self):
        book_url = self.book.get_absolute_url()
        response = self.client.get(book_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)
        self.assertContains(response, self.book.isbn)

    def test_non_exists_book_detail_page_redirects_to_book_list(self):
        url = reverse('books:book_detail', kwargs={'isbn': 1444001})
        response = self.client.get(url, follow=True)
        self.assertTemplateUsed(response, 'books/book_list.html')


class BookCreateViewTest(TestCase):
    def setUp(self):
        UserModel = get_user_model()
        self.username = 'test'
        self.password = 'GreaterThan8'
        self.user = UserModel.objects.create_user(
            self.username, 'test@mail.com', self.password
        )
        self.author = AuthorFactory()
        self.publisher = PublisherFactory()

    def test_create_book_login_required(self):
        url = reverse('books:book_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_create_book_successfully(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('books:book_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        payload = {
            'title': 'test book',
            'isbn': '123456',
            'pages': 100,
            'author': self.author.id,
            'publisher': self.publisher.id,
        }
        response = self.client.post(url, data=payload, follow=True)
        self.assertContains(response, '123456 was created successfully')

    def test_create_book_with_invalid_isbn_failed(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('books:book_create')
        payload = {
            'title': 'test book',
            'isbn': 'isbn',
            'pages': 100,
            'author': self.author.id,
            'publisher': self.publisher.id,
        }
        response = self.client.post(url, data=payload, follow=True)
        self.assertContains(response, 'The creation has failed.')
        self.assertFormError(
            response, 'form', 'isbn', 'Only digits and hyphen are allowed.'
        )

    def test_create_book_with_missing_isbn_failed(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('books:book_create')
        payload = {
            'title': 'test book',
            'isbn': '',
            'pages': 100,
            'author': self.author.id,
            'publisher': self.publisher.id,
        }
        response = self.client.post(url, data=payload, follow=True)
        self.assertContains(response, 'The creation has failed.')
        self.assertFormError(response, 'form', 'isbn', 'This field is required.')

    def test_create_book_with_existed_isbn_failed(self):
        book = BookFactory(isbn=100)
        self.client.login(username=self.username, password=self.password)
        url = reverse('books:book_create')
        payload = {
            'title': 'test book',
            'isbn': book.isbn,
            'pages': 100,
            'author': self.author.id,
            'publisher': self.publisher.id,
        }
        response = self.client.post(url, data=payload, follow=True)
        self.assertContains(response, 'The creation has failed.')
        self.assertFormError(
            response, 'form', 'isbn', f'Book with ISBN {book.isbn} already exists.'
        )


class BookUpdateViewTest(TestCase):
    def setUp(self):
        UserModel = get_user_model()
        self.username = 'test'
        self.password = 'GreaterThan8'
        self.user = UserModel.objects.create_user(
            self.username, 'test@mail.com', self.password
        )

    def test_update_book_successfully(self):
        self.client.login(username=self.username, password=self.password)
        book = BookFactory(isbn=1234)
        url = reverse('books:book_update', kwargs={'isbn': book.isbn})
        payload = model_to_dict(book)
        payload['title'] = 'Unique book title'
        payload['pages'] = 50
        response = self.client.post(url, data=payload, follow=True)
        self.assertContains(response, f'{book.isbn} was updated successfully')
        self.assertContains(response, 'Unique book title')


class BookDeleteViewTest(TestCase):
    def setUp(self):
        UserModel = get_user_model()
        self.username = 'test'
        self.password = 'GreaterThan8'
        self.user = UserModel.objects.create_user(
            self.username, 'test@mail.com', self.password
        )

    def test_delete_book_successfully(self):
        self.client.login(username=self.username, password=self.password)
        book = BookFactory()
        url = reverse('books:book_delete', kwargs={'isbn': book.isbn})
        response = self.client.post(url, follow=True)
        self.assertContains(response, f'{book.isbn} was deleted successfully')
        self.assertEqual(Book.objects.count(), 0)
