from django.db import models
from django.db.models import Q


class BooksManager(models.Manager):
    def get_queryset(self):
        return (
            super(BooksManager, self)
            .get_queryset()
            .select_related('author', 'publisher')
        )

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(title__icontains=query)
                | Q(author__first_name__icontains=query)
                | Q(author__last_name__icontains=query)
                | Q(publisher__name__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs
