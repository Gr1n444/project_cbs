from django.contrib import admin
from app_test.models import Tests, Question, Answer, Result, Choice

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Tests)
admin.site.register(Answer)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Result)