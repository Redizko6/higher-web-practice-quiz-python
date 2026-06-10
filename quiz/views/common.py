"""Общие функции для контроллеров приложения quiz."""

from collections.abc import Callable

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response

ModelSerializer = type[serializers.ModelSerializer]


def collection_response(
    request: Request,
    serializer_class: ModelSerializer,
    list_objects: Callable[[], list[models.Model]],
    create_object: Callable[[dict], models.Model],
) -> Response:
    """Обработать стандартные GET и POST для коллекции сущностей."""
    if request.method == 'GET':
        return Response(serializer_class(list_objects(), many=True).data)

    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    instance = create_object(dict(serializer.validated_data))
    return Response(
        serializer_class(instance).data, status=status.HTTP_201_CREATED
    )


def detail_response(
    request: Request,
    object_id: int,
    serializer_class: ModelSerializer,
    get_object: Callable[[int], models.Model],
    update_object: Callable[[int, dict], models.Model],
    delete_object: Callable[[int], None],
    not_found_message: str,
) -> Response:
    """Обработать стандартные GET, PUT и DELETE для одной сущности."""
    try:
        instance = get_object(object_id)
        if request.method == 'GET':
            return Response(serializer_class(instance).data)
        if request.method == 'DELETE':
            delete_object(object_id)
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated = update_object(object_id, serializer.validated_data)
        return Response(serializer_class(updated).data)
    except ObjectDoesNotExist:
        return Response(
            {'detail': not_found_message}, status=status.HTTP_404_NOT_FOUND
        )
