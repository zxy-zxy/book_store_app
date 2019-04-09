from django.urls import path

from .views import (
    AuthorListView,
    PublisherListView,
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    SearchView,
)

app_name = 'books'

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('author/', AuthorListView.as_view(), name='author_list'),
    path('publisher/', PublisherListView.as_view(), name='publisher_list'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('search/', SearchView.as_view(), name='search'),
    path('<slug:isbn>/update/', BookUpdateView.as_view(), name='book_update'),
    path('<slug:isbn>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('<slug:isbn>/', BookDetailView.as_view(), name='book_detail'),
]
