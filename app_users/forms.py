from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.forms import ModelForm, FileInput
from app_users.models import Profile
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    subject = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Тема письма'})
    )
    body = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Ваше сообщение', 'rows': 10, 'cols': 30})
    )
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['captcha'].widget.attrs.update({'placeholder': 'Введите код с картинки'})

    def clean(self):
        cleaned_data = super().clean()
        captcha = cleaned_data.get('captcha')

        if captcha is None:
            self.add_error('captcha', 'Неправильный код капчи')

        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Пароль'})
    )
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['captcha'].widget.attrs.update({'class': 'input-field', 'placeholder': 'Введите код с картинки'})

    def clean(self):
        cleaned_data = super().clean()
        captcha = cleaned_data.get('captcha')
        if captcha is None:
            self.add_error('captcha', 'Неправильный код капчи')
        return cleaned_data

class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'input-field'}),
    )

    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'input-field'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Имя',
            'email': 'Email', 
            'username': 'Логин', 
            'password1': 'Пароль', 
            'password2': 'Подтверждение пароля'
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input-field', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'input-field', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'input-field', 'placeholder': 'Подтверждение пароля'})
        self.fields['captcha'].widget.attrs.update({'class': 'input-field', 'placeholder': 'Введите код с картинки'})

    def clean(self):
        cleaned_data = super().clean()
        captcha = cleaned_data.get('captcha')
        if captcha is None:
            self.add_error('captcha', 'Неправильный код капчи')
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким адресом электронной почты уже существует")
        
        return email


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'about', 
                'city', 'image',
                ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия', 
            'city': 'Город', 
            'about': 'Подробнее о себе',
            'image': 'Аватар профиля'
        }
        widgets = {
            'image': FileInput(),
        }
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        # for field in self.fields.items():
        #     field.widget.attrs.update({'class': 'form-control input-box form-ensurance-header-control'})

class UserForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label="",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "Email", "class": "black-placeholder"}),
    )

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        # for field in self.fields:
        #     self.fields[field].widget.attrs.update({
        #         'class': 'form-control',
        #         'autocomplete': 'off'
        #     })

class UserSetNewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "placeholder": "New password", "class": "black-placeholder"}),
        strip=False,
    )

    new_password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "placeholder": "Confirm New password", "class": "black-placeholder"}),
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for field in self.fields:
        #     self.fields[field].widget.attrs.update({
        #         'class': 'form-control',
        #         'autocomplete': 'off'
        #     })