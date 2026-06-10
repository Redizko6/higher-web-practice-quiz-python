"""Модуль c роутингом."""

from django.urls import path

from quiz.views.category import category_collection, category_detail
from quiz.views.question import (
    check_answer,
    question_collection,
    question_detail,
    questions_by_text,
)
from quiz.views.quiz import (
    quiz_collection,
    quiz_detail,
    quizzes_by_title,
    random_question,
)

urlpatterns = [
    path('category', category_collection, name='category-create'),
    path('category', category_collection, name='category-get-by-id'),
    path('category', category_collection, name='category-list'),
    path(
        'category/<int:category_id>', category_detail, name='category-detail'
    ),
    path(
        'category/<int:category_id>', category_detail, name='category-update'
    ),
    path(
        'category/<int:category_id>', category_detail, name='category-delete'
    ),
    path('question', question_collection, name='question-list-create'),
    path('question', question_collection, name='question-create'),
    path('question', question_collection, name='question-get-by-id'),
    path(
        'question/by_text/<str:query>',
        questions_by_text,
        name='question-by-text',
    ),
    path(
        'question/<int:question_id>/check', check_answer, name='question-check'
    ),
    path(
        'question/<int:question_id>', question_detail, name='question-detail'
    ),
    path(
        'question/<int:question_id>', question_detail, name='question-update'
    ),
    path(
        'question/<int:question_id>', question_detail, name='question-delete'
    ),
    path('quiz', quiz_collection, name='quiz-list-create'),
    path('quiz', quiz_collection, name='quiz-create'),
    path('quiz', quiz_collection, name='quiz-get-by-id'),
    path('quiz/by_title/<str:title>', quizzes_by_title, name='quiz-by-title'),
    path(
        'quiz/<int:quiz_id>/random_question',
        random_question,
        name='quiz-random-question',
    ),
    path('quiz/<int:quiz_id>', quiz_detail, name='quiz-detail'),
    path('quiz/<int:quiz_id>', quiz_detail, name='quiz-update'),
    path('quiz/<int:quiz_id>', quiz_detail, name='quiz-delete'),
]
