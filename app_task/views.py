from django.shortcuts import render, get_object_or_404
from .models import Task, Submission
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required


@cache_page(60*15)
@login_required
def Tasks(request):
    profile = request.user.profile
    tasks = Task.objects.exclude(type_task='event').order_by('-type_task', '-published')
    context = {
        'tasks': tasks, 'profile': profile
    }
    return render(request, 'tasks.html', context)

@login_required
def Events(request):
    profile = request.user.profile
    tasks = Task.objects.filter(type_task='event').order_by('-published')
    context = {
        'tasks': tasks, 'profile': profile
    }
    return render(request, 'events.html', context)

@login_required
@cache_page(60*15)
def view_Task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    profile = request.user.profile
    context = {
        'task': task,
        'is_correct': None,
        'user_answer': '',
        'already_answered': False,
    }

    # Проверяем, существует ли уже правильный ответ пользователя на это задание
    existing_submission = Submission.objects.filter(task=task, user=request.user, is_correct=True).exists()
    if existing_submission:
        context['already_answered'] = True

    if request.method == 'POST':
        user_answer = request.POST.get('user_answer', '')
        points = task.points

        if not context['already_answered']:  # Проверяем, проходил ли пользователь задание
            if user_answer.strip().lower() == task.correct_answer.lower():
                is_correct = True
                profile.points += points

                if profile.points >= 100:
                    profile.level = 'Advanced'
                elif profile.points >= 50:
                    profile.level = 'Intermediate'
                else:
                    profile.level = 'Beginner'
                profile.save(update_fields=['points', 'level'])

                Submission.objects.create(task=task, user=request.user, user_answer=user_answer, is_correct=is_correct)
            else:
                is_correct = False
                Submission.objects.create(task=task, user=request.user, user_answer=user_answer, is_correct=is_correct)

            context['is_correct'] = is_correct
            context['user_answer'] = user_answer

    return render(request, 'view_task.html', context)

@login_required
@cache_page(60*15)
def view_Event(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    profile = request.user.profile
    context = {
        'task': task,
        'is_correct': None,
        'user_answer': '',
        'already_answered': False,
    }

    # Проверяем, существует ли уже правильный ответ пользователя на это задание
    existing_submission = Submission.objects.filter(task=task, user=request.user, is_correct=True).exists()
    if existing_submission:
        context['already_answered'] = True

    if request.method == 'POST':
        user_answer = request.POST.get('user_answer', '')
        points = task.points

        if not context['already_answered']:  # Проверяем, проходил ли пользователь задание
            if user_answer.strip().lower() == task.correct_answer.lower():
                is_correct = True
                profile.event_points += points

                profile.save(update_fields=['event_points'])

                Submission.objects.create(task=task, user=request.user, user_answer=user_answer, is_correct=is_correct)
            else:
                is_correct = False
                Submission.objects.create(task=task, user=request.user, user_answer=user_answer, is_correct=is_correct)

            context['is_correct'] = is_correct
            context['user_answer'] = user_answer

    return render(request, 'view_event.html', context)