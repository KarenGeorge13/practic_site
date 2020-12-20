from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .models import Article, Comment, User
from .forms import CommentForm, UserRegisterForm, UserLoginForm, EditProfileForm, AddNewsForm, SearchForm
# Create your views here.


def index(request):
    news = Article.objects.all()
    return render(request, 'news/index.html', {'news': news})


def search(request):
    news = None
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_str = form.cleaned_data.get('search')
            news = Article.objects.filter(title__icontains=search_str)
    else:
        form = SearchForm()
    return render(request, 'news/search.html', {'form': form, 'news': news})


def view_news(request, news_id):
    news = get_object_or_404(Article, pk=news_id)
    comments = Comment.objects.filter(article=news_id)
    count = comments.count()
    form = CommentForm()
    return render(request, 'news/news.html', {'news': news, 'comments': comments, 'form': form, 'comment_count': count})


def add_comment(request, news_id, user_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            com = Comment()
            com.topic = form.cleaned_data.get('topic')
            com.text = form.cleaned_data.get('text')
            com.user = get_object_or_404(User, pk=user_id)
            com.article = get_object_or_404(Article, pk=news_id)
            com.save()
            return HttpResponseRedirect(reverse('news', kwargs={'news_id': news_id}))


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username=name, email=email, password=password)
            user.save()
            messages.success(request, 'Вы успешно зарегестрировались')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def authen(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def user_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    news = Article.objects.filter(user=user_id)
    return render(request, 'news/profile.html', {'user': user, 'news': news})


def edit_profile(request, user_id):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = get_object_or_404(User, pk=user_id)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.about = form.cleaned_data.get('about')
            if form.cleaned_data.get('photo'):
                user.photo = form.cleaned_data.get('photo')
            user.save()
            return user_profile(request, user_id)
    else:
        form = EditProfileForm(instance=get_object_or_404(User, pk=user_id))
    return render(request, 'news/edit_profile.html', {'form': form})


def add_news(request, user_id):
    if request.method == 'POST':
        form = AddNewsForm(request.POST)
        if form.is_valid():
            article = Article()
            article.title = form.cleaned_data.get('title')
            article.annotation = form.cleaned_data.get('annotation')
            article.text = form.cleaned_data.get('text')
            article.user = get_object_or_404(User, pk=user_id)
            article.save()
            return redirect('home')
    else:
        form = AddNewsForm()
    return render(request, 'news/add_news.html', {'form': form})


def edit_news(request, news_id, user_id):
    article = get_object_or_404(Article, pk=news_id)
    if request.method == 'POST':
        form = AddNewsForm(request.POST)
        if form.is_valid():
            article.title = form.cleaned_data.get('title')
            article.annotation = form.cleaned_data.get('annotation')
            article.text = form.cleaned_data.get('text')
            article.save()
            return user_profile(request, user_id)
    else:
        data = {
            'title': article.title,
            'annotation': article.annotation,
            'text': article.text,
        }
        form = AddNewsForm(data=data)
    return render(request, 'news/edit_news.html', {'form': form, 'news': article})


def delete_news(request, news_id, user_id):
    article = get_object_or_404(Article, pk=news_id)
    article.delete()
    return user_profile(request, user_id)
