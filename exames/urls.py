from django.urls import path
from . import views

urlpatterns = [
    path('solicitarExames/', views.solicitarExames, name='solicitarExames')
]
