from django.urls import path
from . import views

urlpatterns = [
    path('gerenciarClientes/', views.gerenciarClientes, name="gerenciarClientes"),
    path('cliente/<int:cliente_id>', views.cliente, name="cliente"),
    path('exameCliente/<int:exame_id>', views.exameCliente, name="exameCliente"),
    path('proxyPdf/<int:exame_id>', views.proxyPdf, name="proxyPdf"),
    path('gerarSenha/<int:exame_id>', views.gerarSenha, name="gerarSenha"),
]