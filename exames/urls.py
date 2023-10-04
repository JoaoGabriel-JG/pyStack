from django.urls import path
from . import views

urlpatterns = [
    path('solicitarExames/', views.solicitarExames, name='solicitarExames'),
    path('fecharPedido/', views.fecharPedido, name='fecharPedido'),
    path('gerenciarPedidos/', views.gerenciarPedidos, name="gerenciarPedidos"),
    path('cancelarPedido/<int:pediodoId>', views.cancelarPedido, name='cancelarPedido'),
]
