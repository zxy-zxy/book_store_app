from django.forms import ModelForm, ValidationError

from .models import Book


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'publisher', 'pages']

    def clean_isbn(self):
        val = self.cleaned_data['isbn']
        if Book.objects.exclude(pk=self.instance.pk).filter(isbn=val):
            raise ValidationError(f'Book with ISBN {val} already exists.')
        return val
