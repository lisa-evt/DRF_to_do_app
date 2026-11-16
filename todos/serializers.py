from rest_framework import serializers

from .models import Board, Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'done', 'created', 'updated')
        read_only_fields = ('id', 'created', 'updated')


class BoardSerializer(serializers.ModelSerializer):
    """Used for create and update, so the response stays small."""

    class Meta:
        model = Board
        fields = ('id', 'name')
        read_only_fields = ('id',)


class BoardListSerializer(BoardSerializer):
    todo_count = serializers.IntegerField(read_only=True)

    class Meta(BoardSerializer.Meta):
        fields = (*BoardSerializer.Meta.fields, 'todo_count')


class BoardDetailSerializer(BoardSerializer):
    todos = TodoSerializer(many=True, read_only=True)

    class Meta(BoardSerializer.Meta):
        fields = (*BoardSerializer.Meta.fields, 'todos')