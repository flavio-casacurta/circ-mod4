# coding: utf-8

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from circulante.catalogo.models import Publicacao

class Participante(models.Model):
    user  = models.OneToOneField(User)
    ativo = models.BooleanField(default=True)	


def criar_rgistro_participante(sender, instance, created, **kwargs):
    if created:
        Participante.objects.create(user=instance)

post_save.connect(criar_rgistro_participante, sender=User)
  
class Clube(models.Model):
    nome=models.CharField(max_length=64)
    descricao=models.CharField(max_length=1024)
    membros = models.ManyToManyField(Participante)
    
OPCOES_STATUS = [
('disponivel', u'disponível'), # disponível para empréstimo
('emprestado', u'emprestado'), # emprestado 
('reservado', u'reservado'),
('privado', u'privado'),
]
    
class Item(models.Model):
    data_aquisicao = models.DateField()
    publicacao = models.ForeignKey(Publicacao)
    proprietario = models.ForeignKey(Participante)
    status = models.CharField(max_length=16, choices=OPCOES_STATUS,
                              default= OPCOES_STATUS[0][0])
    notas =  models.TextField(blank=True)

class Emprestimo(models.Model):
    solicitante = models.ForeignKey(Participante)
    publicacao = models.ForeignKey(Publicacao)
    item=models.ForeignKey(Item, null=True)
    datahora_retirada = models.DateTimeField(null=True)
    datahora_devolucao = models.DateTimeField(null=True)
    data_limite_devolucao = models.DateField(null=True)
    notas =  models.TextField(blank=True)
