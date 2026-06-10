"""Модуль с реализацией сервиса вопросов."""

from quiz.constants import QUESTION_EDITABLE_FIELDS
from quiz.dao import AbstractQuestionService
from quiz.models import Question
from quiz.services.base import BaseModelService


class QuestionService(BaseModelService[Question], AbstractQuestionService):
    """Реализация сервиса для вопросов."""

    model = Question
    editable_fields = QUESTION_EDITABLE_FIELDS

    def list_questions(self) -> list[Question]:
        """Вернуть все вопросы."""
        return self.list_objects()

    def get_question(self, question_id: int) -> Question:
        """Вернуть вопрос по идентификатору."""
        return self.get_object(question_id)

    def get_questions_by_text(self, text: str) -> list[Question]:
        """Вернуть вопросы, текст которых содержит искомую строку."""
        return list(Question.objects.filter(text__icontains=text))

    def get_questions_for_quiz(self, quiz_id: int) -> list[Question]:
        """Вернуть вопросы указанного квиза."""
        return list(Question.objects.filter(quiz_id=quiz_id))

    def create_question(self, quiz_id: int, data: dict) -> Question:
        """Создать вопрос для указанного квиза."""
        question_data = {**data, 'quiz_id': quiz_id}
        question_data.pop('quiz', None)
        if 'category_id' in question_data:
            question_data.pop('category', None)
        elif isinstance(question_data.get('category'), int):
            question_data['category_id'] = question_data.pop('category')
        return self.create_object(question_data)

    def update_question(self, question_id: int, data: dict) -> Question:
        """Обновить вопрос."""
        return self.update_object(question_id, data)

    def delete_question(self, question_id: int) -> None:
        """Удалить вопрос."""
        self.delete_object(question_id)

    def check_answer(self, question_id: int, answer: str) -> bool:
        """Проверить ответ на вопрос."""
        return self.get_question(question_id).correct_answer == answer

    def random_question_from_quiz(self, quiz_id: int) -> Question:
        """Вернуть случайный вопрос квиза."""
        question = (
            Question.objects.filter(quiz_id=quiz_id).order_by('?').first()
        )
        if question is None:
            raise Question.DoesNotExist
        return question
