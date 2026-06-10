"""Модуль с контроллерами для вопросов."""

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from quiz.constants import QUESTION_NOT_FOUND
from quiz.models import Question
from quiz.serializers import QuestionSerializer
from quiz.services.question import QuestionService
from quiz.views.common import collection_response, detail_response

service = QuestionService()


def _create_question(data: dict) -> Question:
    """Подготовить данные сериализатора и создать вопрос."""
    quiz_id = data.pop('quiz').id
    return service.create_question(quiz_id, data)


class AnswerSerializer(serializers.Serializer):
    """Сериализатор ответа пользователя."""

    answer = serializers.CharField(allow_blank=True)


@api_view(['GET', 'POST'])
def question_collection(request: Request) -> Response:
    """Получить список вопросов или создать вопрос."""
    return collection_response(
        request, QuestionSerializer, service.list_questions, _create_question
    )


@api_view(['GET', 'PUT', 'DELETE'])
def question_detail(request: Request, question_id: int) -> Response:
    """Получить, изменить или удалить вопрос."""
    return detail_response(
        request,
        question_id,
        QuestionSerializer,
        service.get_question,
        service.update_question,
        service.delete_question,
        QUESTION_NOT_FOUND,
    )


@api_view(['GET'])
def questions_by_text(request: Request, query: str) -> Response:
    """Получить вопросы по части текста."""
    return Response(
        QuestionSerializer(
            service.get_questions_by_text(query), many=True
        ).data
    )


@api_view(['POST'])
def check_answer(request: Request, question_id: int) -> Response:
    """Проверить ответ пользователя."""
    serializer = AnswerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        is_correct = service.check_answer(
            question_id, serializer.validated_data['answer']
        )
        return Response({'correct': is_correct})
    except ObjectDoesNotExist:
        return Response(
            {'detail': QUESTION_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND
        )
