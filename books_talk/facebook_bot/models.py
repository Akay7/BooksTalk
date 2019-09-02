from django.db import models


class FacebookSender(models.Model):
    SEARCH_BY_TITLE = 'title'
    SEARCH_BY_GOODREADS_ID = 'goodreads_id'
    SEARCH_BY_CHOICES = (
        (SEARCH_BY_TITLE, 'Search by title'),
        (SEARCH_BY_GOODREADS_ID, 'Search by Goodreads id'),
    )

    psid = models.TextField(max_length=20)
    search_by = models.TextField(max_length=16, choices=SEARCH_BY_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.psid
