from django.urls import path
from . import views

urlpatterns = [
    path('solicitarExames/', views.solicitarExames, name='solicitarExames'),
    path('fecharPedido/', views.fecharPedido, name='fecharPedido'),
    path('gerenciarPedidos/', views.gerenciarPedidos, name="gerenciarPedidos"),
    path('cancelarPedido/<int:pediodoId>', views.cancelarPedido, name='cancelarPedido'),
    path('gerenciarExames/', views.gerenciarExames, name="gerenciarExames"),
    path('permitirAbrirExames/<int:exameId>', views.permitirAbrirExames, name="permitirAbrirExames"),
    path('solicitarSenhaExame/<int:exameId>', views.solicitarSenhaExame, name="solicitarSenhaExame"),
    path('gerarAcessoMedico/', views.gerarAcessoMedico, name="gerarAcessoMedico"),
    path('acessoMedico/<str:token>', views.acessoMedico, name="acessoMedico"),
]
