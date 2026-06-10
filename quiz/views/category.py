"""Модуль с контроллерами для категорий."""

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from quiz.constants import CATEGORY_NOT_FOUND
from quiz.serializers import CategorySerializer
from quiz.services.category import CategoryService
from quiz.views.common import collection_response, detail_response

service = CategoryService()


@api_view(['GET', 'POST'])
def category_collection(request: Request) -> Response:
    """Получить список категорий или создать категорию."""
    return collection_response(
        request,
        CategorySerializer,
        service.list_categories,
        lambda data: service.create_category(data['title']),
    )


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request: Request, category_id: int) -> Response:
    """Получить, изменить или удалить категорию."""
    return detail_response(
        request,
        category_id,
        CategorySerializer,
        service.get_category,
        service.update_category,
        service.delete_category,
        CATEGORY_NOT_FOUND,
    )
