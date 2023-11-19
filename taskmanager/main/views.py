from django.shortcuts import render,redirect
from .models import Task
from .forms import TaskForm
from django.db.models import Q
import webbrowser
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests


@login_required(login_url='login')
def index(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request,"main/index.html",{"title":"Главная страница сайта", "tasks":tasks})


def about(request):
    return render(request,"main/about.html")

@login_required(login_url='login')
def create(request):
    error = ""
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            form.save()
            return redirect("home")
        else:
            error = "Неверная форма записи"

    form = TaskForm()
    context ={
        "form": form,
        "error": error
    }
    return render(request,"main/create.html",context)


def delete(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request, 'delete.html', {'task': task})

@login_required(login_url='login')
def search(request):
    query = request.GET.get('q')
    tasks = None
    wikipedia_query = None


    if query:
        tasks = Task.objects.filter(Q(title__icontains=query) | Q(task__icontains=query), user=request.user)

    if request.method == 'GET':
        if query and query.startswith('@'):
            wikipedia_query = query[1:]
            # Выполняем запрос к API Википедии на русском языке
            url = f'https://ru.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext&titles={wikipedia_query}'
            response = requests.get(url)
            data = response.json()

            # Парсим результаты запроса
            pages = data['query']['pages']
            page_id = next(iter(pages))
            extract = pages[page_id]['extract']

            return render(request, 'main/wikipedia_search.html',{'tasks': tasks, 'query': query, 'wikipedia_query': wikipedia_query, 'extract': extract})

        return render(request, 'main/search.html', {'tasks': tasks, 'query': query, 'wikipedia_query': wikipedia_query})



@login_required(login_url='login')
def wikipedia_search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            # Выполняем запрос к API Википедии на русском языке
            url = f'https://ru.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext&titles={query}'
            response = requests.get(url)
            data = response.json()

            # Парсим результаты запроса
            pages = data['query']['pages']
            page_id = next(iter(pages))
            extract = pages[page_id]['extract']


            return render(request, 'main/wikipedia_search.html', {'extract': extract})
        else:
            return render(request, 'main/wikipedia_search.html', {'extract': None})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        return redirect('login')
    return render(request, 'main/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
    return render(request, 'main/login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')