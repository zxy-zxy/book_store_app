from django.urls import path

from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    SearchView,
)

app_name = 'books'

urlpatterns = [
    path('all/', BookListView.as_view(), name='book_list'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('search/', SearchView.as_view(), name='search'),
    path('<slug:isbn>/update/', BookUpdateView.as_view(), name='book_update'),
    path('<slug:isbn>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('<slug:isbn>/', BookDetailView.as_view(), name='book_detail'),
]
