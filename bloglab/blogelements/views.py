from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from blogelements.forms import LoginForm, RegisterForm, CommentForm
from blogelements.models import Article, Comment


# Create your views here.
def home(request):
    article = Article.objects.all()
    context = {
        'articles': article
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html')


def show_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST":
        form = CommentForm(request.POST)  # Получаем данные из формы

        if form.is_valid():  # Проверяем валидность формы
            if request.user.is_authenticated:  # Проверяем авторизацию пользователя
                form.cleaned_data["article"] = article  # Добавляем ключ и значение статьи
                try:
                    Comment.objects.create(**form.cleaned_data)  # Создаем новую запись в таблицу
                    return redirect('article', article_id)  # Обновляем страницу со статьей
                except Exception as Ex:
                    print(Ex)
                    form.add_error(None, 'Ошибка добавления коммента')
            else:
                return redirect("login")
    else:
        form = CommentForm()

    return render(request, 'blog/article.html', {'article': article, 'comment': article.comment_set.all, 'form': form})


def loginPage(request):
    form = LoginForm()

    # обрабатываем случай отправки формы на этот адрес
    if request.method == 'POST':

        # заполянем объект данными, полученными из запроса
        form = LoginForm(request.POST)

        # проверяем валидность формы
        if form.is_valid():
            # пытаемся авторизовать пользователя
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                # если существует пользователь с таким именем и паролем,
                # то сохраняем авторизацию и делаем редирект
                login(request, user)
                return redirect('me')
            else:
                # иначе возвращаем ошибку
                form.add_error(None, 'Неверные данные!')

    # рендерим шаблон и передаем туда объект формы
    return render(request, 'account/login.html', {'form': form})


def registerPage(request):

    # инициализируем объект формы
    form = RegisterForm()

    if request.method == 'POST':
        # заполняем объект данными формы, если она была отправлена
        form = RegisterForm(request.POST)

        if form.is_valid():
            # если форма валидна - создаем нового пользователя
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            return redirect('login')
    # ренедерим шаблон и передаем объект формы
    return render(request, 'account/registration.html', {'form': form})


def me(request):
    # если не авторизован, то редирект на страницу входа
    if not request.user.is_authenticated:
        return redirect('login')
    # рендерим шаблон и передаем туда объект пользователя
    return render(request, 'account/me.html', {'user': request.user})


def doLogout(request):
    # вызываем функцию django.contrib.auth.logout и делаем редирект на страницу входа
    logout(request)
    return redirect('login')
