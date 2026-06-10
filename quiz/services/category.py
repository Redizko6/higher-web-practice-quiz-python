"""Модуль с реализацией сервиса категорий."""

from quiz.constants import CATEGORY_EDITABLE_FIELDS
from quiz.dao import AbstractCategoryService
from quiz.models import Category
from quiz.services.base import BaseModelService


class CategoryService(BaseModelService[Category], AbstractCategoryService):
    """Реализация сервиса для категорий."""

    model = Category
    editable_fields = CATEGORY_EDITABLE_FIELDS

    def list_categories(self) -> list[Category]:
        """Вернуть все категории."""
        return self.list_objects()

    def get_category(self, category_id: int) -> Category:
        """Вернуть категорию по идентификатору."""
        return self.get_object(category_id)

    def create_category(self, title: str) -> Category:
        """Создать категорию."""
        return self.create_object({'title': title})

    def update_category(self, category_id: int, data: dict) -> Category:
        """Обновить категорию."""
        return self.update_object(category_id, data)

    def delete_category(self, category_id: int) -> None:
        """Удалить категорию."""
        self.delete_object(category_id)
