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