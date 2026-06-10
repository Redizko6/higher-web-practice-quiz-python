"""Тесты сервисного слоя."""

import pytest

from quiz.models import Category, Question, Quiz
from quiz.services.category import CategoryService
from quiz.services.question import QuestionService
from quiz.services.quiz import QuizService

pytestmark = pytest.mark.django_db


class TestCategoryService:
    """Тесты сервиса категорий."""

    service = CategoryService()

    def test_list_categories(self, category: Category) -> None:
        """Сервис возвращает список категорий."""
        assert self.service.list_categories() == [category]

    def test_get_category(self, category: Category) -> None:
        """Сервис возвращает категорию по идентификатору."""
        assert self.service.get_category(category.id) == category

    def test_create_category(self) -> None:
        """Сервис создаёт категорию."""
        assert self.service.create_category('History').title == 'History'

    def test_update_category(self, category: Category) -> None:
        """Сервис изменяет категорию."""
        assert (
            self.service.update_category(
                category.id, {'title': 'History'}
            ).title
            == 'History'
        )

    def test_delete_category(self, category: Category) -> None:
        """Сервис удаляет категорию."""
        self.service.delete_category(category.id)
        assert Category.objects.count() == 0


class TestQuizService:
    """Тесты сервиса квизов."""

    service = QuizService()

    def test_list_quizzes(self, quiz: Quiz) -> None:
        """Сервис возвращает список квизов."""
        assert self.service.list_quizzes() == [quiz]

    def test_get_quiz(self, quiz: Quiz) -> None:
        """Сервис возвращает квиз по идентификатору."""
        assert self.service.get_quiz(quiz.id) == quiz

    def test_get_quizes_by_title(self, quiz: Quiz) -> None:
        """Сервис ищет квизы без учёта регистра."""
        assert self.service.get_quizes_by_title('SPA') == [quiz]

    def test_create_quiz(self) -> None:
        """Сервис создаёт квиз."""
        assert (
            self.service.create_quiz({'title': 'History'}).title == 'History'
        )

    def test_update_quiz(self, quiz: Quiz) -> None:
        """Сервис изменяет квиз."""
        assert (
            self.service.update_quiz(quiz.id, {'title': 'Planets'}).title
            == 'Planets'
        )

    def test_delete_quiz(self, quiz: Quiz) -> None:
        """Сервис удаляет квиз."""
        self.service.delete_quiz(quiz.id)
        assert Quiz.objects.count() == 0


class TestQuestionService:
    """Тесты сервиса вопросов."""

    service = QuestionService()

    def test_list_questions(self, question: Question) -> None:
        """Сервис возвращает список вопросов."""
        assert self.service.list_questions() == [question]

    def test_get_question(self, question: Question) -> None:
        """Сервис возвращает вопрос по идентификатору."""
        assert self.service.get_question(question.id) == question

    def test_get_questions_by_text(self, question: Question) -> None:
        """Сервис ищет вопросы без учёта регистра."""
        assert self.service.get_questions_by_text('PLANET') == [question]

    def test_get_questions_for_quiz(self, question: Question) -> None:
        """Сервис возвращает вопросы квиза."""
        assert self.service.get_questions_for_quiz(question.quiz_id) == [
            question
        ]

    def test_create_question(self, question_data: dict, quiz: Quiz) -> None:
        """Сервис создаёт вопрос."""
        assert (
            self.service.create_question(quiz.id, question_data).text
            == question_data['text']
        )

    def test_update_question(self, question: Question) -> None:
        """Сервис изменяет вопрос."""
        assert (
            self.service.update_question(
                question.id, {'difficulty': 'hard'}
            ).difficulty
            == 'hard'
        )

    def test_delete_question(self, question: Question) -> None:
        """Сервис удаляет вопрос."""
        self.service.delete_question(question.id)
        assert Question.objects.count() == 0

    def test_check_correct_answer(self, question: Question) -> None:
        """Сервис принимает правильный ответ."""
        assert self.service.check_answer(question.id, 'Mercury') is True

    def test_check_incorrect_answer(self, question: Question) -> None:
        """Сервис отклоняет неправильный ответ."""
        assert self.service.check_answer(question.id, 'Venus') is False

    def test_random_question_from_quiz(self, question: Question) -> None:
        """Сервис возвращает вопрос указанного квиза."""
        assert (
            self.service.random_question_from_quiz(question.quiz_id)
            == question
        )

    def test_random_question_from_empty_quiz(self, quiz: Quiz) -> None:
        """Сервис сообщает об отсутствии вопросов в квизе."""
        with pytest.raises(Question.DoesNotExist):
            self.service.random_question_from_quiz(quiz.id)
