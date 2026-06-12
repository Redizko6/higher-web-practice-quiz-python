"""Общие константы приложения quiz."""

CATEGORY_TITLE_MAX_LENGTH = 100
QUIZ_TITLE_MAX_LENGTH = 200
DESCRIPTION_MAX_LENGTH = 500
QUESTION_TEXT_MAX_LENGTH = 500
CORRECT_ANSWER_MAX_LENGTH = 500
EXPLANATION_MAX_LENGTH = 250
DIFFICULTY_MAX_LENGTH = 6
MIN_QUESTION_OPTIONS = 2

CATEGORY_FIELDS = ('id', 'title')
QUIZ_FIELDS = ('id', 'title', 'description')
QUESTION_FIELDS = (
    'id',
    'quiz',
    'category',
    'text',
    'description',
    'options',
    'correct_answer',
    'explanation',
    'difficulty',
)
CATEGORY_EDITABLE_FIELDS = ('title',)
QUIZ_EDITABLE_FIELDS = ('title', 'description')
QUESTION_EDITABLE_FIELDS = (
    'quiz',
    'quiz_id',
    'category',
    'category_id',
    'text',
    'description',
    'options',
    'correct_answer',
    'explanation',
    'difficulty',
)

CATEGORY_NOT_FOUND = 'Категория не найдена.'
QUIZ_NOT_FOUND = 'Квиз не найден.'
QUESTION_NOT_FOUND = 'Вопрос не найден.'
QUIZ_QUESTION_NOT_FOUND = 'Квиз или вопрос не найден.'
OPTIONS_VALIDATION_ERROR = 'Укажите как минимум два варианта ответа.'
CORRECT_ANSWER_VALIDATION_ERROR = (
    'Правильный ответ должен входить в список вариантов.'
)
