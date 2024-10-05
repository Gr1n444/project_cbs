from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import F
from app_test.models import Tests, Question, Answer, Result, Choice
from django.views.decorators.cache import cache_page

@cache_page(60*15)
@login_required
def tests(request):
    profile = request.user.profile
    tests = Tests.objects.all()
    context = {'tests': tests, 'profile': profile}
    return render(request, 
                'tests.html', context)


@login_required
def display_test(request, test_id):
    test = get_object_or_404(Tests, pk=test_id)
    question = test.question_set.first()
    return redirect(reverse('app_test:display_question', 
        kwargs={'test_id': test_id, 
                'question_id': question.pk}))


@login_required
def display_question(request, test_id, question_id):
    profile = request.user.profile
    test = get_object_or_404(Tests, pk=test_id)
    questions = test.question_set.all()
    current_question, next_question = None, None
    current_index = None  # Переменная для хранения индекса текущего вопроса

    for ind, question in enumerate(questions):
        if question.pk == question_id:
            current_question = question
            current_index = ind + 1  # Индексация с 1
            if ind != len(questions) - 1:
                next_question = questions[ind + 1]
            break  # Прерываем цикл, так как вопрос найден

    context = {
        'test': test, 
        'question': current_question,
        'number': len(questions),
        'next_question': next_question, 
        'profile': profile,
        'current_index': current_index  # Добавляем индекс текущего вопроса в контекст
    }
    
    return render(request, 'display.html', context)


@login_required
def grade_question(request, test_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    test = get_object_or_404(Tests, pk=test_id)
    can_answer = question.user_can_answer(request.user)
    profile = request.user.profile

    try:
        if not can_answer:
            return render(request, 'partial.html', {'question': question, 'error_message': 'Вы уже отвечали на этот вопрос.'})

        if question.qtype == 'single':
            correct_answer = question.get_answers()
            user_answer = question.answer_set.get(pk=request.POST['answer'])
            is_correct = correct_answer == user_answer

            choice = Choice(user=request.user, question=question, answer=user_answer)
            choice.save()

            result, created = Result.objects.get_or_create(user=request.user, test=test)
            if is_correct:
                result.correct = F('correct') + 1
                profile.points += 10
            else:
                result.wrong = F('wrong') + 1
            result.save()

        elif question.qtype == 'multiple':
            correct_answer = question.get_answers()
            answers_ids = request.POST.getlist('answer')
            user_answers = []
            if answers_ids:
                for answer_id in answers_ids:
                    user_answer = Answer.objects.get(pk=answer_id)
                    user_answers.append(user_answer.name)
                    choice = Choice(user=request.user, question=question, answer=user_answer)
                    choice.save()
                is_correct = correct_answer == user_answers
                
                result, created = Result.objects.get_or_create(user=request.user, test=test)
                if is_correct:
                    result.correct = F('correct') + 1
                    profile.points += 10
                else:
                    result.wrong = F('wrong') + 1
                result.save()
        
        if profile.points >= 100:
            profile.level = 'Advanced'
        elif profile.points >= 50:
            profile.level = 'Intermediate'
        else:
            profile.level = 'Beginner'
        profile.save(update_fields=['points', 'level'])

    except Exception as e:
        return render(request, 'partial.html', {'question': question})

    return render(request, 'partial.html', {'is_correct': is_correct, 'correct_answer': correct_answer, 'question': question})


@login_required
def test_results(request, test_id):
    profile = request.user.profile
    test = get_object_or_404(Tests, pk=test_id)
    questions = test.question_set.all()
    results = Result.objects.filter(user=request.user, 
        test=test).values()
    correct = [i['correct'] for i in results][0]
    wrong = [i['wrong'] for i in results][0]
    context = {'test': test, 
    'profile': profile, 
    'correct': correct, 
    'wrong': wrong, 
    'number': len(questions), 
    'skipped': len(questions) - (correct + wrong)}
    return render(request, 
        'results.html', context)
