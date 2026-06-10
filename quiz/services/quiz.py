"""Модуль с реализацией сервиса квизов."""

from quiz.constants import QUIZ_EDITABLE_FIELDS
from quiz.dao import AbstractQuizService
from quiz.models import Quiz
from quiz.services.base import BaseModelService


class QuizService(BaseModelService[Quiz], AbstractQuizService):
    """Реализация сервиса для квиза."""

    model = Quiz
    editable_fields = QUIZ_EDITABLE_FIELDS

    def list_quizzes(self) -> list[Quiz]:
        """Вернуть все квизы."""
        return self.list_objects()

    def get_quiz(self, quiz_id: int) -> Quiz:
        """Вернуть квиз по идентификатору."""
        return self.get_object(quiz_id)

    def get_quizes_by_title(self, title: str) -> list[Quiz]:
        """Вернуть квизы, название которых содержит искомую строку."""
        return list(Quiz.objects.filter(title__icontains=title))

    def create_quiz(self, data: dict) -> Quiz:
        """Создать квиз."""
        return self.create_object(data)

    def update_quiz(self, quiz_id: int, data: dict) -> Quiz:
        """Обновить квиз."""
        return self.update_object(quiz_id, data)

    def delete_quiz(self, quiz_id: int) -> None:
        """Удалить квиз."""
        self.delete_object(quiz_id)
