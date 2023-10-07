from django.contrib import messages
from django.contrib.messages import constants
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib.admin.views.decorators import staff_member_required
from empresarial.utils import gerarPdfExames, gerarSenhaAleatoria
from exames.models import SolicitacaoExame


@staff_member_required
def gerenciarClientes(request):
    clientes = User.objects.filter(is_staff=False)

    nomeCompleto = request.GET.get('nome')
    email = request.GET.get('email')

    if email:
        clientes = clientes.filter(email__contains = email)
    if nomeCompleto:
        clientes = clientes.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).filter(full_name__contains=nomeCompleto)

    return render(request, 'gerenciarClientes.html', {'clientes': clientes, 'nomeCompleto': nomeCompleto, 'email': email})

@staff_member_required
def cliente(request, cliente_id):
    cliente = User.objects.get(id=cliente_id)
    exames = SolicitacaoExame.objects.filter(usuario=cliente)
    return render(request, 'cliente.html', {'cliente': cliente, 'exames': exames})

@staff_member_required
def exameCliente(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    return render(request, 'exameCliente.html', {'exame': exame})

@staff_member_required
def proxyPdf(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)

    response = exame.resultado.open()
    return FileResponse(response)

@staff_member_required
def gerarSenha(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)

    if exame.senha:
        # Baixar o documento da senha já existente
        return FileResponse(gerarPdfExames(exame.exame.nome, exame.usuario, exame.senha), filename="token.pdf")

    senha = gerarSenhaAleatoria(9)
    exame.senha = senha
    exame.save()
    return FileResponse(gerarPdfExames(exame.exame.nome, exame.usuario, exame.senha), filename="token.pdf")


@staff_member_required
def alterarDadosExame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)

    pdf = request.FILES.get('resultado')
    status = request.POST.get('status')
    requer_senha = request.POST.get('requer_senha')

    if requer_senha and (not exame.senha):
        messages.add_message(request, constants.ERROR, 'Para exigir a senha primeiro crie uma.')
        return redirect(f'/empresarial/exameCliente/{exame_id}')

    exame.requer_senha = True if requer_senha else False

    if pdf:
        exame.resultado = pdf

    exame.status = status
    exame.save()
    messages.add_message(request, constants.SUCCESS, 'Alteração realizada com sucesso')
    return redirect(f'/empresarial/exameCliente/{exame_id}')
