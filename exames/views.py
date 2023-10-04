from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TiposExames

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
    examesId = request.POST.get('exames')
    print(examesId)

    return HttpResponse('Estou aqui')
