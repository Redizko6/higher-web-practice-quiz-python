"""Модуль c сериализаторами."""

from rest_framework import serializers

from quiz.constants import (
    CATEGORY_FIELDS,
    CORRECT_ANSWER_VALIDATION_ERROR,
    MIN_QUESTION_OPTIONS,
    OPTIONS_VALIDATION_ERROR,
    QUESTION_FIELDS,
    QUIZ_FIELDS,
)
from quiz.models import Category, Question, Quiz


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        """Настройки сериализатора категорий."""

        model = Category
        fields = CATEGORY_FIELDS


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для вопросов."""

    class Meta:
        """Настройки сериализатора вопросов."""

        model = Question
        fields = QUESTION_FIELDS

    def validate_options(self, options: object) -> list[object]:
        """Проверить, что передано не менее двух вариантов ответа."""
        if (
            not isinstance(options, list)
            or len(options) < MIN_QUESTION_OPTIONS
        ):
            raise serializers.ValidationError(OPTIONS_VALIDATION_ERROR)
        return options

    def validate(self, attrs: dict) -> dict:
        """Проверить, что правильный ответ присутствует среди вариантов."""
        options = attrs.get('options', getattr(self.instance, 'options', None))
        correct_answer = attrs.get(
            'correct_answer', getattr(self.instance, 'correct_answer', None)
        )
        if (
            options is not None
            and correct_answer is not None
            and correct_answer not in options
        ):
            raise serializers.ValidationError(
                {'correct_answer': CORRECT_ANSWER_VALIDATION_ERROR}
            )
        return attrs


class QuizSerializer(serializers.ModelSerializer):
    """Сериализатор для квизов."""

    class Meta:
        """Настройки сериализатора квизов."""

        model = Quiz
        fields = QUIZ_FIELDS
