from django.db import models
from django.contrib.auth.models import User

class Material(models.Model):
    nome = models.CharField(max_length=250)
    descricao = models.TextField()
    quantidade_disponivel = models.PositiveIntegerField()
    imagem = models.ImageField(upload_to='materials/', blank=True, null=True)
    
    def __str__(self):
        return self.nome
    
class Retirada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)    
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(null=int)
    data_retirada = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.usuario.username} - {self.material.nome} ({self.quantidade})'