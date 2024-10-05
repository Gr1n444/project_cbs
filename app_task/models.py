from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    task_title = models.CharField(max_length=30, default='Task')
    task_text = models.TextField()
    task_description = models.TextField()
    type_task = models.CharField(max_length=255, default='')
    correct_answer = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    difficulty = models.CharField(max_length=200, default="Легкое")
    published = models.DateTimeField(auto_now_add=True)
    title_image = models.ImageField(upload_to='task_images/', blank=True, null=True)
    material_file = models.FileField(upload_to='task_materials/', blank=True, null=True)

    def __str__(self) -> str:
        return self.task_title
    
    class Meta:
        verbose_name = 'Задание CTF для одиночных пользователей'
        verbose_name_plural = 'Задания CTFs для одиночных пользователей'

class Submission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task.task_text} - {self.user_answer}"
    
    class Meta:
        verbose_name = 'Ответ пользователя на задания CTF'
        verbose_name_plural = 'Ответы пользователей на задания CTF'
