
# Documentação: Sistema de Controle de Estoque e Almoxarifado com Django
## Índice
- Introdução
- Requisitos
- Estrutura do Projeto
- Configuração do Ambiente
- Criação do Projeto Django
- Configuração do Aplicativo Django
- Definição dos Modelos
- Criação dos Formulários
- Definição das Views
- Configuração das URLs
- Criação dos Templates
- Testes e Migrações
- Execução do Servidor de Desenvolvimento
- Conclusão

## 1. Introdução

Este documento detalha o processo de criação de um sistema de controle de estoque e almoxarifado usando Django. O sistema permitirá a retirada e devolução de materiais, listará os usuários que não devolveram materiais, e incluirá uma área administrativa para gerenciar usuários e materiais.

## 2. Requisitos
- Python 3.11
- Django 5.0.4

## 3. Estrutura do Projeto

O projeto será estruturado da seguinte maneira:

```bash
  estoque/
├── inventario/
│   ├── migrations/
│   ├── templates/
│   │   └── inventario/
│   │       ├── home.html
│   │       ├── listar_materiais.html
│   │       ├── registrar_retirada.html
│   │       ├── listar_devedores.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── estoque/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```
## 4. Configuração do Ambiente

Criação do Ambiente Virtual

Criar Ambiente Virtual

```bash
python -m venv venv
```
Inicializar ambiente virtual(Windows)

```bash
venv\Scripts\activate  # Windows
```
Inicializar Ambiente Virtual(Linux/MacOS)
```bash
source venv/bin/activate  # Linux/MacOS
```
Instalar o Django
```bash
pip Install django
```

## 5. Criação do Projeto Django

Criar Projeto
```bash
django-admin startproject estoque
cd estoque
```
## 6. Configuração do Aplicativo Django
Criação do Aplicativo
```bash
python manage.py startapp inventario
```
Adicionar o app ao 'estoque/settings' em INSTALLED_APPS
```bash
INSTALLED_APPS = [
    ...
    'inventario',
]
```
## 7. Definição dos Modelos
Modelos em inventario/models.py

Criar as models para Materiais e Retirada
```bash
from django.db import models
from django.contrib.auth.models import User

class Material(models.Model):
    nome = models.CharField(max_length=100)
    quantidade_disponivel = models.PositiveIntegerField()

    def __str__(self):
        return self.nome

class Retirada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_retirada = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.material.nome} ({self.quantidade})"
```
## 8. Criação dos Formulários
Formulários em inventario/forms.py

Criar os Formulários MaterialForm e RetiradaForm

```bash
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nome', 'descricao', 'quantidade_disponivel', 'imagem']

class RetiradaForm(forms.ModelForm):
    class Meta:
        model = Retirada
        fields = ['material', 'quantidade']

RetiradaFormSet = forms.modelformset_factory(Retirada, form=RetiradaForm, extra=1)

```


## 9. Definição das Views
Views em inventario/views.py

Definir as Views 

```bash
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Material, Retirada
from .forms import RetiradaFormSet

def home(request):
    return render(request, 'inventario/home.html')

@login_required
def listar_materiais(request):
    materiais = Material.objects.all()
    return render(request, 'inventario/listar_materiais.html', {'materiais': materiais})

@login_required
def registrar_retirada(request):
    if request.method == 'POST':
        formset = RetiradaFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:  
                    retirada = form.save(commit=False)
                    retirada.usuario = request.user
                    retirada.save()
                    material = retirada.material
                    material.quantidade_disponivel -= retirada.quantidade
                    material.save()
            return redirect('listar_materiais')
    else:
        formset = RetiradaFormSet(queryset=Retirada.objects.none())
    return render(request, 'inventario/registrar_retirada.html', {'formset': formset})

@login_required
def listar_devedores(request):
    retiradas = Retirada.objects.filter(data_devolucao__isnull=True)
    return render(request, 'inventario/listar_devedores.html', {'retiradas': retiradas})
```
## 10. Configuração das URLs
URLs em inventario/urls.py

``` bash
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('materiais/', views.listar_materiais, name='listar_materiais'),
    path('retirada/', views.registrar_retirada, name='registrar_retirada'),
    path('devedores/', views.listar_devedores, name='listar_devedores'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
```
URLs em estoque/urls.py

``` bash
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventario.urls')),
]
```

## 11. Criação dos Templates
Template home.html

``` bash
<!DOCTYPE html>
<html>
<head>
    <title>Home</title>
</head>
<body>
    <h1>Bem-vindo ao Sistema de Controle de Estoque</h1>
    <p>Use os links abaixo para navegar pelo sistema:</p>
    <ul>
        <li><a href="{% url 'listar_materiais' %}">Listar Materiais</a></li>
        <li><a href="{% url 'registrar_retirada' %}">Registrar Retirada</a></li>
        <li><a href="{% url 'listar_devedores' %}">Listar Devedores</a></li>
    </ul>
</body>
</html>
``` 

Template listar_materiais.html

``` bash
<!DOCTYPE html>
<html>
<head>
    <title>Listar Materiais</title>
</head>
<body>
    <h1>Materiais</h1>
    <ul>
        {% for material in materiais %}
            <li>{{ material.nome }} - Quantidade Disponível: {{ material.quantidade_disponivel }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```
Template registrar_retirada.html
```bash
<!DOCTYPE html>
<html>
<head>
    <title>Registrar Retirada</title>
</head>
<body>
    <h1>Registrar Retirada</h1>
    <form method="post">
        {% csrf_token %}
        {{ formset.management_form }}
        {% for form in formset %}
            {{ form.as_p }}
        {% endfor %}
        <button type="submit">Registrar</button>
    </form>
</body>
</html>
```
Template listar_devedores.html

```bash
<!DOCTYPE html>
<html>
<head>
    <title>Listar Devedores</title>
</head>
<body>
    <h1>Devedores</h1>
    <ul>
        {% for retirada in retiradas %}
            <li>{{ retirada.usuario.username }} - {{ retirada.material.nome }} - Quantidade: {{ retirada.quantidade }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```
## 12. Testes e Migrações
Aplicar Migrações
```bash
python manage.py makemigrations
python manage.py migrate
```
Criar um Superusuário

```bash
python manage.py createsuperuser
```
## 13. Execução do Servidor de Desenvolvimento

Executar no navegador
```bash
python manage.py runserver
```
## 14. Conclusão
Este foi um sistema básico de controle de estoque e almoxarifado funcional usando Django que criei. O sistema permite listar materiais, registrar retiradas, listar devedores e inclui uma área administrativa para gerenciar usuários e materiais.