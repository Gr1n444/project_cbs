from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from app_users.forms import ContactForm, LoginForm, CustomUserCreationForm, ProfileForm, UserForgotPasswordForm, UserSetNewPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .models import Profile
from django.views.decorators.cache import cache_page


@cache_page(60*15)
def landing(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            msg = f'Пользователь {name} с email {email} сообщает:\n\n{body}'
            try: 
                send_mail(
                    subject=subject,
                    message=msg,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.RECIPIENT_ADDRESS]
                )
                messages.success(request, 'Сообщение отправлено! Администрация сайта ответит Вам в ближайшее время.')
                return redirect('landing')
            except Exception as e:
                messages.error(request, f'Ошибка при отправке сообщения: {str(e)}')
        else:
            if 'captcha' in form.errors:
                messages.error(request, 'Неправильный код капчи')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ContactForm()
    return render(request, 'landing.html', {'form': form})

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('account')
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next', 'account'))
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
        else:
            if 'captcha' in form.errors:
                messages.error(request, 'Неправильный код капчи')

    return render(request, 'login.html', {'form': form})

@login_required
def logoutUser(request):
    logout(request)
    messages.info(request, 'Вы вышли из учетной записи')
    return redirect('landing')

def registerUser(request):
    if request.user.is_authenticated:
        return redirect('account')
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.is_active = False
            user.save()
            profile = Profile.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
            )
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_url = reverse_lazy('confirm_email', kwargs={'uidb64': uid, 'token': token})
            send_mail(
                'Подтвердите свой электронный адрес',
                f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{"127.0.0.1:8000"}{activation_url}',
                'danilf259@yandex.ru',
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Аккаунт успешно создан! На Ваш почтовый ящик направлено письмо с ссылкой на завершение регистрации')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    context = {'page': page, 'form': form}
    return render(request, 'register.html', context)


def UserConfirmEmailView(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Ваш электронный адрес подтвержден!')
    else:
        messages.success(request, 'При активации почты произошла ошибка, обратитесь к администратору сайта.')
    return redirect('account')

class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    form_class = UserForgotPasswordForm
    template_name = 'user_password_reset.html'
    success_url = reverse_lazy('register')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлено на указанный email'
    subject_template_name = 'password_subject_reset_mail.txt'
    email_template_name = 'password_reset_mail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context

class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = UserSetNewPasswordForm
    template_name = 'user_password_set_new.html'
    success_url = reverse_lazy('login')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context

def userProfile(request, username):
    profile = Profile.objects.get(username=username)
    context = {'profile': profile}
    return render(request, 'profile_user.html', context)

@login_required
def userAccount(request):
    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'account.html', context)

@login_required
def editUserAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, 
            instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'edit_account.html', context)

@cache_page(60*15)
def leaderboardUsers(request):
    users = Profile.objects.all().order_by('-points')
    return render(request, 'rating.html', {'users': users})

@cache_page(60*15)
def leaderboardEvent(request):
    users = Profile.objects.all().order_by('-event_points')
    return render(request, 'event_rating.html', {'users': users})