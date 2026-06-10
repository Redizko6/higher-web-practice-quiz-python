
"""Тесты метаданных моделей приложения quiz."""

import pytest
from django.db import models

from quiz.models import Category, Question, Quiz


@pytest.mark.parametrize(
    ('model', 'expected_verbose_name'),
    [
        (Category, 'категория'),
        (Quiz, 'квиз'),
        (Question, 'вопрос'),
    ],
)
def test_model_verbose_name(
    model: type[models.Model], expected_verbose_name: str
) -> None:
    """Модель содержит человекочитаемое название."""
    assert model._meta.verbose_name == expected_verbose_name


@pytest.mark.parametrize(
    ('model', 'expected_verbose_name_plural'),
    [
        (Category, 'категории'),
        (Quiz, 'квизы'),
        (Question, 'вопросы'),
    ],
)
def test_model_verbose_name_plural(
    model: type[models.Model], expected_verbose_name_plural: str
) -> None:
    """Модель содержит человекочитаемое название во множественном числе."""
    assert model._meta.verbose_name_plural == expected_verbose_name_plural


@pytest.mark.parametrize(
    ('model', 'field_name', 'expected_verbose_name'),
    [
        (Category, 'title', 'название'),
        (Quiz, 'title', 'название'),
        (Quiz, 'description', 'описание'),
        (Question, 'quiz', 'квиз'),
        (Question, 'category', 'категория'),
        (Question, 'text', 'текст вопроса'),
        (Question, 'description', 'описание'),
        (Question, 'options', 'варианты ответа'),
        (Question, 'correct_answer', 'правильный ответ'),
        (Question, 'explanation', 'объяснение ответа'),
        (Question, 'difficulty', 'сложность'),
    ],
)
def test_field_verbose_name(
    model: type[models.Model],
    field_name: str,
    expected_verbose_name: str,
) -> None:
    """Поле модели содержит человекочитаемое название."""
    assert (
        model._meta.get_field(field_name).verbose_name == expected_verbose_name
    )
