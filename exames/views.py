from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TiposExames, PedidosExames, SolicitacaoExame


@login_required()
def solicitarExames(request):
    tiposExames = TiposExames.objects.all()

    if request.method == 'GET':

        return render(request, 'solicitarExames.html', {'tiposExames': tiposExames})

    elif request.method == 'POST':
        examesId = request.POST.getlist('exames')
        solicitacaoExames = TiposExames.objects.filter(id__in=examesId)
        precoTotal = 0

        for i in solicitacaoExames:
            if i.disponivel:
                precoTotal += i.preco

        return render(request, 'solicitarExames.html', {
                                                                                'tiposExames': tiposExames,
                                                                                'solicitacaoExames': solicitacaoExames,
                                                                                'precoTotal': precoTotal
                                                                            })
@login_required()
def fecharPedido(request):
    examesId = request.POST.getlist('exames')
    solicitacaoExames = TiposExames.objects.filter(id__in=examesId)

    pedidoExame = PedidosExames(
        usuario=request.user,
        data=datetime.now()
    )

    pedidoExame.save()

    for exame in solicitacaoExames:
        solicitacaoExamesTemp = SolicitacaoExame(
            usuario=request.user,
            exame=exame,
            status='E'
        )
        solicitacaoExamesTemp.save()
        pedidoExame.exames.add(solicitacaoExamesTemp)

    pedidoExame.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido de exame realizado com sucesso')

    return redirect('/exames/gerenciarPedidos/')

@login_required
def gerenciarPedidos(request):
    pedidosExames = PedidosExames.objects.filter(usuario=request.user)
    return render(request, 'gerenciarPedidos.html', {'pedidosExames': pedidosExames})

@login_required
def cancelarPedido(request, pediodoId):
    pedido = PedidosExames.objects.get(id=pediodoId)

    if not pedido.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'Você não tem permissão para cancelar este pedido')
        return redirect('/exames/gerenciarPedidos/')

    pedido.agendado = False
    pedido.save()
    messages.add_message(request, constants.SUCCESS, 'Pedido cancelado com sucesso')

    return redirect('/exames/gerenciarPedidos/')

@login_required()
def gerenciarExames(request):
    exames = SolicitacaoExame.objects.filter(usuario=request.user)

    return render(request, 'gerenciarExames.html', {'exames': exames})

@login_required()
def permitirAbrirExames(request, exameId):
    exame = SolicitacaoExame.objects.get(id=exameId)

    if not exame.requerSenha:
        return redirect(exame.resultado.url)
    elif not exame.resultado:
        messages.add_message(request, constants.ERROR, 'PDF inexistente ou inválido')
        return redirect('/exames/gerenciarExames')

    return redirect(f'/exames/solicitarSenhaExame/{exameId}')

@login_required()
def solicitarSenhaExame(request, exameId):
    exame = SolicitacaoExame.objects.get(id=exameId)

    if request.method == 'GET':
        return render(request, 'solicitarSenhaExame.html', {'exame': exame})
    elif request.method == 'POST':
        senha = request.POST.get('senha')
        if senha == exame.senha and exame.resultado:
            return redirect(exame.resultado.url)
        elif not exame.resultado:
            messages.add_message(request, constants.ERROR, 'PDF inexistente ou inválido')
            return redirect(f'/exames/gerenciarExames')
        else:
            messages.add_message(request, constants.ERROR, 'Senha incorreta')
            return redirect(f'/exames/solicitarSenhaExame/{exameId}')


