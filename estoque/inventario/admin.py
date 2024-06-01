from django.contrib import admin
from .models import Material, Retirada

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'quantidade_disponivel')
    search_fields = ('nome',)

@admin.register(Retirada)
class RetiradaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'material', 'data_retirada', 'data_devolucao')
    search_fields = ('usuario__username', 'material__nome')