from django.urls import path
from . import views

urlpatterns = [
    path('gerenciarClientes/', views.gerenciarClientes, name="gerenciarClientes"),
    path('cliente/<int:cliente_id>', views.cliente, name="cliente"),
]