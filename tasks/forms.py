from django import forms
from django.forms import ModelForm
from .models import Task, Product


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity']
