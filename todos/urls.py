from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import BoardViewSet, TodoViewSet, BOARD_URL_KWARG

router = SimpleRouter()
router.register('boards', BoardViewSet, basename='board')

TODO_LIST_ACTIONS = {'get': 'list', 'post': 'create'}
TODO_DETAIL_ACTIONS = {
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
}

urlpatterns = [
    path(
        f'boards/<int:{BOARD_URL_KWARG}>/todos/',
        TodoViewSet.as_view(TODO_LIST_ACTIONS),
        name='todo-list',
    ),
    path(
        f'boards/<int:{BOARD_URL_KWARG}>/todos/<int:pk>/',
        TodoViewSet.as_view(TODO_DETAIL_ACTIONS),
        name='todo-detail',
    ),
    *router.urls,
]