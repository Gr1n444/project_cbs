from django.db import models
from django.contrib.auth.models import User


class Tests(models.Model):
    name = models.CharField(max_length=120)
    published = models.DateTimeField(auto_now_add=True)
    test_description = models.CharField(max_length=120, default="Описание теста")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['published']
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

class Question(models.Model):
    class qtype(models.TextChoices):
        single = 'single'
        multiple = 'multiple'
    
    name = models.CharField(max_length=350)
    qtype = models.CharField(max_length=8, choices=qtype.choices, default=qtype.single)
    task = models.ForeignKey(Tests, on_delete=models.CASCADE)
    explanation = models.CharField(max_length=550)


    def get_answers(self):
        if self.qtype == 'single':
            return self.answer_set.filter(is_correct=True).first()
        else:
            qs = self.answer_set.filter(is_correct=True).values()
            return [i.get('name') for i in qs]

    def user_can_answer(self, user):
        user_choices = user.choice_set.all()
        done = user_choices.filter(question=self)
        print(done)
        if done.exists():
            return False
        return True

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

class Result(models.Model):
    test = models.ForeignKey(Tests, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'

class Choice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Выбор пользователя'
        verbose_name_plural = 'Выборы пользователей'