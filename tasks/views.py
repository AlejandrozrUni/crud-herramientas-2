from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm, ProductoForm
from .models import Task, Product
from django.utils import timezone
# Create your views here.
def home(request):
    return render(request, 'home.html')
    
def signup(request):
    
    if request.method == 'GET':
        return render(request, 'signup.html', {
        'form': UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], 
                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error":'el usuario ya existe'
                })
        return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error":'la contraseña no coinciden'
        })
        
        
        
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html',{'tasks': tasks})

def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by
    ('-datecompleted')
    return render(request, 'tasks.html',{'tasks': tasks})

def create_task(request):
    if request.method == 'GET':
            return render(request, 'create_task.html',{
                'form': TaskForm
            })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html',{
                'form': TaskForm,
                "error":'proporciona datos validos'
            })

def task_detail(request,task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html',{
            'task':task,
            'form': form
            })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html',{
            'task':task,
            'form': form,
            'error':'error actualizando tarea'
            })
            
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm
    })
    else:
        user=authenticate(
            request, username=request.POST['username'], 
            password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error':'usuario o contraseña incorrecta'
                })
        else:
            login(request, user)
            return redirect('tasks')

def products(request):
    products = Product.objects.filter(user=request.user)
    return render(request, 'products.html', {'products': products})

def create_product(request):
    if request.method == 'GET':
        return render(request, 'create_product.html', {
            'form': ProductoForm
        })
    else:
        try:
            form = ProductoForm(request.POST)
            new_product = form.save(commit=False)
            new_product.user = request.user
            new_product.save()
            return redirect('products')
        except ValueError:
            return render(request, 'create_product.html', {
                'form': ProductoForm,
                'error': 'Datos proporcionados no válidos'
            })

def product_detail(request, product_id):
    if request.method == 'GET':
        product = get_object_or_404(Product, pk=product_id, user=request.user)
        form = ProductoForm(instance=product)
        return render(request, 'product_detail.html', {
            'product': product,
            'form': form
        })
    else:
        try:
            product = get_object_or_404(Product, pk=product_id, user=request.user)
            form = ProductoForm(request.POST, instance=product)
            form.save()
            return redirect('products')
        except ValueError:
            return render(request, 'product_detail.html', {
                'product': product,
                'form': form,
                'error': 'Error al actualizar el producto'
            })

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id, user=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('products')