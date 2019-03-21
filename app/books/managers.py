from django.db import models


class BooksManager(models.Manager):
    def get_queryset(self):
        return (
            super(BooksManager, self)
            .get_queryset()
            .select_related('author', 'publisher')
        )
