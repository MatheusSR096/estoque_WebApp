from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('materiais/', views.listar_materiais, name='listar_materiais'),
    path('retirada/', views.registrar_retirada, name='registrar_retirada'),
    path('devedores/', views.listar_devedores, name='listar_devedores'),
]
