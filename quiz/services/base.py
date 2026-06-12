"""Общие операции сервисного слоя."""

from typing import Generic, TypeVar

from django.db import models
from django.shortcuts import get_object_or_404

ModelT = TypeVar('ModelT', bound=models.Model)


class BaseModelService(Generic[ModelT]):
    """Переиспользуемые CRUD-операции над Django-моделями."""

    model: type[ModelT]
    editable_fields: tuple[str, ...] = ()

    def list_objects(self) -> list[ModelT]:
        """Вернуть все объекты модели."""
        return list(self.model.objects.all())

    def get_object(self, object_id: int) -> ModelT:
        """Вернуть объект модели по идентификатору."""
        return get_object_or_404(self.model, pk=object_id)

    def create_object(self, data: dict) -> ModelT:
        """Проверить и сохранить новый объект модели."""
        instance = self.model(**data)
        instance.full_clean()
        instance.save()
        return instance

    def update_object(self, object_id: int, data: dict) -> ModelT:
        """Изменить разрешённые поля объекта модели."""
        instance = self.get_object(object_id)
        for field, value in data.items():
            if field in self.editable_fields:
                setattr(instance, field, value)
        instance.full_clean()
        instance.save()
        return instance

    def delete_object(self, object_id: int) -> None:
        """Удалить объект модели."""
        self.get_object(object_id).delete()
