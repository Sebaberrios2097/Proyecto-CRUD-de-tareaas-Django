from django.shortcuts import render, redirect, get_object_or_404 as get_objects
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Tasks 
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    #funcion para registrar usuarios
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
    
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #registrar usuario
                user = User.objects.create_user(username=request.POST['username'], 
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                form = UserCreationForm()
                return render(request, 'signup.html', {'form': form, 'error': 'El usuario ya existe'})
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form, 'error': 'Las contraseñas no coinciden'})

@login_required
def tasks(request):
    #función para solo mostrar las tareas del usuario logueado
    if request.user.is_authenticated:
        tareas = Tasks.objects.filter(usuario=request.user, fecha_completado__isnull=True).order_by('-fecha_creacion')
        return render(request, 'tasks.html', {'tareas': tareas})
    else:
        return redirect('home')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            form = AuthenticationForm()
            return render(request, 'signin.html', {'form': form, 'error': 'Usuario o contraseña incorrectos'})
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def createTask(request):
    if request.method == 'GET':
        form = TaskForm()
        return render(request, 'create_task.html', {'form': form})
    else:
        try:
            form = TaskForm(request.POST)
            newTask = form.save(commit=False)
            newTask.usuario = request.user
            newTask.save()
            return redirect('tasks')
        except ValueError:
            form = TaskForm()
            return render(request, 'create_task.html', {'form': form, 'error': 'Datos incorrectos'})

@login_required
def task_detail(request, id):
    #Función para editar tarea que sean solo de un usuario
    tarea = get_objects(Tasks, pk=id, usuario=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=tarea)
        return render(request, 'task_detail.html', {'tarea': tarea, 'form': form})
    else:
        try:
            form = TaskForm(request.POST, instance=tarea)
            form.save()
            return redirect('tasks')
        except ValueError:
            form = TaskForm(instance=tarea)
            return render(request, 'task_detail.html', {'tarea': tarea, 'form': form, 'error': 'Datos incorrectos'})

@login_required
def completeTask(request, id):
    tarea = get_objects(Tasks, pk=id, usuario=request.user)
    if request.method == 'POST':
        tarea.fecha_completado = timezone.now()
        tarea.save()
        return redirect('tasks')

@login_required
def deleteTask(request, id):
    #función para eliminar tareas que sean solo de un usuario
    tarea = get_objects(Tasks, pk=id, usuario=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect('tasks')
    else:
        return print('No se ha eliminado nada')

@login_required
def tasksCompleted(request):
    #función para solo mostrar las tareas del usuario logueado
    if request.user.is_authenticated:
        tareas = Tasks.objects.filter(usuario=request.user, fecha_completado__isnull=False).order_by('-fecha_completado')
        return render(request, 'tasks.html', {'tareas': tareas})
