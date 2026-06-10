"""Настройки административной панели приложения quiz."""

from django.contrib import admin

from quiz.models import Category, Question, Quiz


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Отображение категорий в административной панели."""

    list_display = ('id', 'title')
    search_fields = ('title',)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Отображение квизов в административной панели."""

    list_display = ('id', 'title')
    search_fields = ('title', 'description')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Отображение вопросов в административной панели."""

    list_display = ('id', 'text', 'quiz', 'category', 'difficulty')
    list_filter = ('difficulty', 'quiz', 'category')
    search_fields = ('text', 'description')
