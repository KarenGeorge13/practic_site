from django import forms
from .models import Comment, User, Article
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm


class SearchForm(forms.Form):
    search = forms.CharField(label='Поиск по заголовку новости', widget=forms.TextInput(attrs={'class': 'form-control'}))


class AddNewsForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'annotation', 'text']
        labels = {
            'title': 'Заголовок новости',
            'annotation': 'Краткое содержание новости',
            'text': 'Текст новости'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'label': 'Добавить новость'}),
            'annotation': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
        }


class EditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'about', 'photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'photo': forms.FileInput(attrs={'class': 'form-control'})
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Адрес электронной почты', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['topic', 'text']
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 6})
        }
