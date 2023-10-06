from datetime import timedelta, timezone
from secrets import token_urlsafe
from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe


class TiposExames(models.Model):
    tipoChoices = (
        ('I', 'Examde de imagem'),
        ('S', 'Exame de sangue')
    )
    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=1, choices=tipoChoices)
    preco = models.FloatField()
    disponivel = models.BooleanField(default=True)
    horarioInicial = models.IntegerField()
    horarioFinal = models.IntegerField()

    def __str__(self):
        return self.nome

class SolicitacaoExame(models.Model):
    choiceStatus = (
        ('E', 'Em análise'),
        ('F', 'Finalizadd')
    )
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exame = models.ForeignKey(TiposExames, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=choiceStatus)
    resultado = models.FileField(upload_to='resultados', null=True, blank=True)
    requerSenha = models.BooleanField(default=False)
    senha = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return f'{self.usuario} | {self.exame.nome}'

    def badgeTemplate(self):
        classesCss = ''
        texto = ''

        if self.status == 'E':
            classesCss = 'bg-warning text-dark'
            texto = "Em análise"
        elif self.status == 'F':
            classesCss = 'bg-success'
            texto = "Finalizado"

        return mark_safe(f"<span class='badge bg-primary {classesCss}'>{texto}</span>")

class PedidosExames(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exames = models.ManyToManyField(SolicitacaoExame)
    agendado = models.BooleanField(default=True)
    data = models.DateField()

    def __str__(self):
        return f'{self.usuario} | {self.data}'

class AcessoMedico(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    identificacao = models.CharField(max_length=50)
    tempoDeAcesso = models.IntegerField()  # Em horas
    criadoEm = models.DateTimeField()
    dataExamesIniciais = models.DateField()
    dataExamesFinais = models.DateField()
    token = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.token

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = token_urlsafe(6)

        super(AcessoMedico, self).save(*args, **kwargs)

    @property
    def status(self):
        return 'Expirado' if timezone.now() > (self.criadoEm + timedelta(hours=self.tempoDeAcesso)) else 'Ativo'
