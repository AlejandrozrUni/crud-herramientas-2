from django.forms import ModelForm
from .models import Task, Producto


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        
class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'cantidad', 'precio']