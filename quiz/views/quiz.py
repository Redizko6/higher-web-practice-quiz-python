"""Модуль с контроллерами для квизов."""

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from quiz.constants import QUIZ_NOT_FOUND, QUIZ_QUESTION_NOT_FOUND
from quiz.serializers import QuestionSerializer, QuizSerializer
from quiz.services.question import QuestionService
from quiz.services.quiz import QuizService
from quiz.views.common import collection_response, detail_response

service = QuizService()
question_service = QuestionService()


@api_view(['GET', 'POST'])
def quiz_collection(request: Request) -> Response:
    """Получить список квизов или создать квиз."""
    return collection_response(
        request, QuizSerializer, service.list_quizzes, service.create_quiz
    )


@api_view(['GET', 'PUT', 'DELETE'])
def quiz_detail(request: Request, quiz_id: int) -> Response:
    """Получить, изменить или удалить квиз."""
    return detail_response(
        request,
        quiz_id,
        QuizSerializer,
        service.get_quiz,
        service.update_quiz,
        service.delete_quiz,
        QUIZ_NOT_FOUND,
    )


@api_view(['GET'])
def quizzes_by_title(request: Request, title: str) -> Response:
    """Получить квизы по части названия."""
    return Response(
        QuizSerializer(service.get_quizes_by_title(title), many=True).data
    )


@api_view(['GET'])
def random_question(request: Request, quiz_id: int) -> Response:
    """Получить случайный вопрос квиза."""
    try:
        service.get_quiz(quiz_id)
        question = question_service.random_question_from_quiz(quiz_id)
        return Response(QuestionSerializer(question).data)
    except ObjectDoesNotExist:
        return Response(
            {'detail': QUIZ_QUESTION_NOT_FOUND},
            status=status.HTTP_404_NOT_FOUND,
        )
