import factory
import factory.fuzzy
from .models import Book, Publisher, Author


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    first_name = factory.Sequence(lambda n: 'First name #%s' % n)
    last_name = factory.Sequence(lambda n: 'Last name #%s' % n)


class PublisherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Publisher

    name = factory.Sequence(lambda n: 'Name #%s' % n)


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    isbn = factory.Sequence(lambda n: '%s' % n)
    title = factory.Sequence(lambda n: 'Title #%s' % n)
    publisher = factory.SubFactory(PublisherFactory)
    author = factory.SubFactory(AuthorFactory)
