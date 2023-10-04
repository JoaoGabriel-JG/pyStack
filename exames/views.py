from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
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

        #TO DO: Calcular preco dos dados disponiveis

        for i in solicitacaoExames:
            if i.disponivel:
                precoTotal += i.preco

        return render(request, 'solicitarExames.html', {
                                                                                'tiposExames': tiposExames,
                                                                                'solicitacaoExames': solicitacaoExames,
                                                                                'precoTotal': precoTotal
                                                                            })

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

    return redirect('/exames/verPedidos/')

