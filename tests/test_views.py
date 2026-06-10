"""Тесты REST API категорий, квизов и вопросов."""

import pytest
from django.test import Client

from quiz.models import Category, Question, Quiz

pytestmark = pytest.mark.django_db


class TestCategoryAPI:
    """Тесты API категорий."""

    def test_create_category_status(self, client: Client) -> None:
        """Создание категории возвращает 201."""
        response = client.post(
            '/api/category',
            {'title': 'History'},
            content_type='application/json',
        )
        assert response.status_code == 201

    def test_list_categories_content(
        self, client: Client, category: Category
    ) -> None:
        """Список содержит созданную категорию."""
        assert client.get('/api/category').json() == [
            {'id': category.id, 'title': category.title}
        ]

    def test_get_category_content(
        self, client: Client, category: Category
    ) -> None:
        """Получение по id возвращает категорию."""
        assert (
            client.get(f'/api/category/{category.id}').json()['title']
            == category.title
        )

    def test_update_category_content(
        self, client: Client, category: Category
    ) -> None:
        """Изменение возвращает новое название."""
        response = client.put(
            f'/api/category/{category.id}',
            {'title': 'History'},
            content_type='application/json',
        )
        assert response.json()['title'] == 'History'

    def test_delete_category_status(
        self, client: Client, category: Category
    ) -> None:
        """Удаление категории возвращает 204."""
        assert client.delete(f'/api/category/{category.id}').status_code == 204

    def test_get_missing_category_status(self, client: Client) -> None:
        """Для отсутствующей категории возвращается 404."""
        assert client.get('/api/category/999').status_code == 404


class TestQuizAPI:
    """Тесты API квизов."""

    def test_create_quiz_status(self, client: Client) -> None:
        """Создание квиза возвращает 201."""
        response = client.post(
            '/api/quiz', {'title': 'History'}, content_type='application/json'
        )
        assert response.status_code == 201

    def test_list_quizzes_content(self, client: Client, quiz: Quiz) -> None:
        """Список содержит созданный квиз."""
        assert client.get('/api/quiz').json()[0]['id'] == quiz.id

    def test_get_quiz_content(self, client: Client, quiz: Quiz) -> None:
        """Получение по id возвращает квиз."""
        assert client.get(f'/api/quiz/{quiz.id}').json()['title'] == quiz.title

    def test_update_quiz_content(self, client: Client, quiz: Quiz) -> None:
        """Изменение возвращает новое название."""
        response = client.put(
            f'/api/quiz/{quiz.id}',
            {'title': 'Planets', 'description': quiz.description},
            content_type='application/json',
        )
        assert response.json()['title'] == 'Planets'

    def test_delete_quiz_status(self, client: Client, quiz: Quiz) -> None:
        """Удаление квиза возвращает 204."""
        assert client.delete(f'/api/quiz/{quiz.id}').status_code == 204

    def test_get_quizzes_by_title_content(
        self, client: Client, quiz: Quiz
    ) -> None:
        """Поиск по названию возвращает подходящий квиз."""
        assert client.get('/api/quiz/by_title/spa').json()[0]['id'] == quiz.id

    def test_random_question_content(
        self, client: Client, question: Question
    ) -> None:
        """Случайный вопрос принадлежит квизу."""
        assert (
            client.get(f'/api/quiz/{question.quiz_id}/random_question').json()[
                'id'
            ]
            == question.id
        )

    def test_random_question_from_empty_quiz_status(
        self, client: Client, quiz: Quiz
    ) -> None:
        """Пустой квиз возвращает 404."""
        assert (
            client.get(f'/api/quiz/{quiz.id}/random_question').status_code
            == 404
        )


class TestQuestionAPI:
    """Тесты API вопросов."""

    def test_create_question_status(
        self, client: Client, question_data: dict
    ) -> None:
        """Создание вопроса возвращает 201."""
        response = client.post(
            '/api/question', question_data, content_type='application/json'
        )
        assert response.status_code == 201

    def test_create_question_with_one_option_status(
        self, client: Client, question_data: dict
    ) -> None:
        """Один вариант ответа отклоняется."""
        question_data['options'] = ['Mercury']
        response = client.post(
            '/api/question', question_data, content_type='application/json'
        )
        assert response.status_code == 400

    def test_create_question_with_unknown_answer_status(
        self, client: Client, question_data: dict
    ) -> None:
        """Ответ вне списка вариантов отклоняется."""
        question_data['correct_answer'] = 'Earth'
        response = client.post(
            '/api/question', question_data, content_type='application/json'
        )
        assert response.status_code == 400

    def test_list_questions_content(
        self, client: Client, question: Question
    ) -> None:
        """Список содержит созданный вопрос."""
        assert client.get('/api/question').json()[0]['id'] == question.id

    def test_get_question_content(
        self, client: Client, question: Question
    ) -> None:
        """Получение по id возвращает вопрос."""
        assert (
            client.get(f'/api/question/{question.id}').json()['text']
            == question.text
        )

    def test_update_question_content(
        self, client: Client, question: Question
    ) -> None:
        """Изменение возвращает новую сложность."""
        data = {
            'quiz': question.quiz_id,
            'category': question.category_id,
            'text': question.text,
            'options': question.options,
            'correct_answer': question.correct_answer,
            'difficulty': 'hard',
        }
        response = client.put(
            f'/api/question/{question.id}',
            data,
            content_type='application/json',
        )
        assert response.json()['difficulty'] == 'hard'

    def test_delete_question_status(
        self, client: Client, question: Question
    ) -> None:
        """Удаление вопроса возвращает 204."""
        assert client.delete(f'/api/question/{question.id}').status_code == 204

    def test_get_questions_by_text_content(
        self, client: Client, question: Question
    ) -> None:
        """Поиск по тексту возвращает подходящий вопрос."""
        assert (
            client.get('/api/question/by_text/planet').json()[0]['id']
            == question.id
        )

    def test_check_correct_answer_content(
        self, client: Client, question: Question
    ) -> None:
        """Проверка подтверждает правильный ответ."""
        response = client.post(
            f'/api/question/{question.id}/check',
            {'answer': 'Mercury'},
            content_type='application/json',
        )
        assert response.json() == {'correct': True}

    def test_check_incorrect_answer_content(
        self, client: Client, question: Question
    ) -> None:
        """Проверка отклоняет неправильный ответ."""
        response = client.post(
            f'/api/question/{question.id}/check',
            {'answer': 'Venus'},
            content_type='application/json',
        )
        assert response.json() == {'correct': False}

    def test_check_missing_question_status(self, client: Client) -> None:
        """Проверка отсутствующего вопроса возвращает 404."""
        response = client.post(
            '/api/question/999/check',
            {'answer': 'Mercury'},
            content_type='application/json',
        )
        assert response.status_code == 404
