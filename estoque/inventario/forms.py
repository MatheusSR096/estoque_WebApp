from django import forms
from .models import Material, Retirada

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nome', 'descricao', 'quantidade_disponivel', 'imagem']

class RetiradaForm(forms.ModelForm):
    class Meta:
        model = Retirada
        fields = ['material', 'quantidade']

RetiradaFormSet = forms.modelformset_factory(Retirada, form=RetiradaForm, extra=1)
