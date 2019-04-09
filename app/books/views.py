from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import Book, Publisher, Author
from .forms import BookForm


class HomePageView(TemplateView):
    template_name = 'home.html'


class AuthorListView(ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'books/author_list.html'
    paginate_by = 10


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'books/author_detail.html'
    context_object_name = 'author'


class PublisherListView(ListView):
    model = Publisher
    context_object_name = 'publisher_list'
    template_name = 'books/publisher_list.html'
    paginate_by = 10


class PublisherDetailView(DetailView):
    model = Publisher
    context_object_name = 'publisher'
    template_name = 'books/publisher_detail.html'


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'book_list'
    paginate_by = 3

    def get_queryset(self, **kwargs):
        query = self.request.GET.get('q', None)
        if query is None:
            return super().get_queryset(**kwargs)
        qs = Book.objects.search(query)
        return qs


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    slug_field = 'isbn'
    slug_url_kwarg = 'isbn'

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return redirect('books:book_list')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context_data = super(BookDetailView, self).get_context_data(**kwargs)
        return context_data


class BookCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_message = '%(isbn)s was created successfully'

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'The creation has failed.')
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context_data = super(BookCreateView, self).get_context_data()
        context_data['action_url'] = reverse_lazy('books:book_create')
        context_data['action_text'] = 'Create'
        return context_data


class BookUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Book
    form_class = BookForm
    slug_url_kwarg = 'isbn'
    slug_field = 'isbn'
    template_name = 'books/book_form.html'
    success_message = '%(isbn)s was updated successfully'

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'The update has failed.')
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context_data = super(BookUpdateView, self).get_context_data()
        context_data['action_url'] = reverse_lazy(
            'books:book_update', kwargs={'isbn': self.kwargs['isbn']}
        )
        context_data['action_text'] = 'Update'
        return context_data


class BookDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Book
    slug_field = 'isbn'
    slug_url_kwarg = 'isbn'
    success_url = reverse_lazy('books:book_list')
    context_object_name = 'book'
    template_name = 'books/book_confirm_delete.html'

    def get_success_url(self):
        if self.success_url:
            isbn = self.kwargs['isbn']
            messages.add_message(
                self.request, messages.SUCCESS, f'{isbn} was deleted successfully.'
            )
            return self.success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")

    def get(self, request, *args, **kwargs):
        try:
            self.model.objects.get(isbn=kwargs['isbn'])
            return super(BookDeleteView, self).get(request, *args, **kwargs)
        except self.model.DoesNotExist:
            return redirect('books:book_list')
