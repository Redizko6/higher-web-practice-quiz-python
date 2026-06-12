"""Модуль c моделями приложения quiz."""

from django.core.exceptions import ValidationError
from django.db import models

from quiz.constants import (
    CATEGORY_TITLE_MAX_LENGTH,
    CORRECT_ANSWER_MAX_LENGTH,
    CORRECT_ANSWER_VALIDATION_ERROR,
    DESCRIPTION_MAX_LENGTH,
    DIFFICULTY_MAX_LENGTH,
    EXPLANATION_MAX_LENGTH,
    MIN_QUESTION_OPTIONS,
    OPTIONS_VALIDATION_ERROR,
    QUESTION_TEXT_MAX_LENGTH,
    QUIZ_TITLE_MAX_LENGTH,
)


class Category(models.Model):
    """Модель категории вопросов."""

    title = models.CharField(
        'название', max_length=CATEGORY_TITLE_MAX_LENGTH, unique=True
    )

    class Meta:
        """Метаданные модели категории."""

        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self) -> str:
        """Вернуть название категории."""
        return self.title


class Quiz(models.Model):
    """Модель квиза."""

    title = models.CharField('название', max_length=QUIZ_TITLE_MAX_LENGTH)
    description = models.CharField(
        'описание', max_length=DESCRIPTION_MAX_LENGTH, blank=True, default=''
    )

    class Meta:
        """Метаданные модели квиза."""

        verbose_name = 'квиз'
        verbose_name_plural = 'квизы'

    def __str__(self) -> str:
        """Вернуть название квиза."""
        return self.title


class Difficulty(models.TextChoices):
    """Варианты сложностей для вопросов."""

    EASY = 'easy', 'Лёгкий'
    MEDIUM = 'medium', 'Средний'
    HARD = 'hard', 'Сложный'


class Question(models.Model):
    """Модель вопроса."""

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='квиз',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='категория',
    )
    text = models.CharField(
        'текст вопроса', max_length=QUESTION_TEXT_MAX_LENGTH
    )
    description = models.CharField(
        'описание', max_length=DESCRIPTION_MAX_LENGTH, blank=True, default=''
    )
    options = models.JSONField('варианты ответа')
    correct_answer = models.CharField(
        'правильный ответ', max_length=CORRECT_ANSWER_MAX_LENGTH
    )
    explanation = models.CharField(
        'объяснение ответа',
        max_length=EXPLANATION_MAX_LENGTH,
        blank=True,
        default='',
    )
    difficulty = models.CharField(
        'сложность',
        max_length=DIFFICULTY_MAX_LENGTH,
        choices=Difficulty.choices,
    )

    class Meta:
        """Метаданные модели вопроса."""

        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def clean(self) -> None:
        """Проверить варианты ответа и правильный ответ."""
        super().clean()
        if (
            not isinstance(self.options, list)
            or len(self.options) < MIN_QUESTION_OPTIONS
        ):
            raise ValidationError({'options': OPTIONS_VALIDATION_ERROR})
        if self.correct_answer not in self.options:
            raise ValidationError(
                {'correct_answer': CORRECT_ANSWER_VALIDATION_ERROR}
            )

    def __str__(self) -> str:
        """Вернуть текст вопроса."""
        return self.text
