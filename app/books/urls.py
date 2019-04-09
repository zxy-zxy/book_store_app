from django.urls import path

from .views import (
    AuthorListView,
    AuthorDetailView,
    PublisherListView,
    PublisherDetailView,
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

app_name = 'books'

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('author/', AuthorListView.as_view(), name='author_list'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
    path('publisher/', PublisherListView.as_view(), name='publisher_list'),
    path('publisher/<int:pk>', PublisherDetailView.as_view(), name='publisher_detail'),
    path('<slug:isbn>/update/', BookUpdateView.as_view(), name='book_update'),
    path('<slug:isbn>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('<slug:isbn>/', BookDetailView.as_view(), name='book_detail'),
]
