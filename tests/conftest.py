"""Общие фикстуры тестов Quiz API."""

import pytest

from quiz.models import Category, Question, Quiz


@pytest.fixture
def category() -> Category:
    """Создать категорию."""
    return Category.objects.create(title='Science')


@pytest.fixture
def quiz() -> Quiz:
    """Создать квиз."""
    return Quiz.objects.create(title='Space', description='Astronomy')


@pytest.fixture
def question_data(category: Category, quiz: Quiz) -> dict:
    """Вернуть данные корректного вопроса для API."""
    return {
        'quiz': quiz.id,
        'category': category.id,
        'text': 'Closest planet to the Sun?',
        'description': 'Choose a planet',
        'options': ['Mercury', 'Venus'],
        'correct_answer': 'Mercury',
        'explanation': 'Mercury has the smallest orbit.',
        'difficulty': 'easy',
    }


@pytest.fixture
def question(category: Category, quiz: Quiz) -> Question:
    """Создать вопрос."""
    return Question.objects.create(
        quiz=quiz,
        category=category,
        text='Closest planet to the Sun?',
        options=['Mercury', 'Venus'],
        correct_answer='Mercury',
        difficulty='easy',
    )
