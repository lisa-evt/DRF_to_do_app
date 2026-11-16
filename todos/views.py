from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from rest_framework import viewsets

from .models import Board
from .serializers import (
    BoardDetailSerializer,
    BoardListSerializer,
    BoardSerializer,
    TodoSerializer,
)


BOARD_URL_KWARG = 'board_pk'


class BoardViewSet(viewsets.ModelViewSet):
    """Boards of the current user only."""

    serializer_classes = {
        'list': BoardListSerializer,
        'retrieve': BoardDetailSerializer,
    }
    ordering_fields = ('name', 'id')
    search_fields = ('name',)

    def get_queryset(self):
        boards = Board.objects.filter(owner=self.request.user)
        if self.action == 'list':
            return boards.annotate(todo_count=Count('todos'))
        if self.action == 'retrieve':
            return boards.prefetch_related('todos')
        return boards

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, BoardSerializer)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TodoViewSet(viewsets.ModelViewSet):
    """Todos of one board; the board must belong to the current user."""

    serializer_class = TodoSerializer
    filterset_fields = ('done',)
    ordering_fields = ('created', 'updated', 'title')
    search_fields = ('title',)

    @cached_property
    def board(self):
        return get_object_or_404(
            Board,
            pk=self.kwargs[BOARD_URL_KWARG],
            owner=self.request.user,
        )

    def get_queryset(self):
        return self.board.todos.all()

    def perform_create(self, serializer):
        serializer.save(board=self.board)