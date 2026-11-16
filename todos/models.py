from django.conf import settings
from django.db import models

NAME_MAX_LENGTH = 100


class Board(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='boards',
    )
    name = models.CharField(max_length=NAME_MAX_LENGTH)

    class Meta:
        ordering = ('name', 'id')

    def __str__(self):
        return self.name


class Todo(models.Model):
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='todos',
    )
    title = models.CharField(max_length=NAME_MAX_LENGTH)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created', '-id')
        indexes = [models.Index(fields=['board', 'done'])]

    def __str__(self):
        return self.title
