import os
from random import choice, shuffle
import string
from django.conf import settings
from django.template.loader import render_to_string
from io import BytesIO
from weasyprint import HTML


def gerarSenhaAleatoria(tamanho):
    caracteresEspeciais = string.punctuation
    caracteres = string.ascii_letters
    numerosList = string.digits

    sobra = 0
    qtd = tamanho // 3
    if not tamanho % 3 == 0:
        sobra = tamanho - qtd

    letras = ''
    for i in range(0, qtd + sobra):
        letras += choice(caracteres)

    numeros = ''
    for i in range(0, qtd):
        numeros += choice(numerosList)

    especiais = ''
    for i in range(0, qtd):
        especiais += choice(caracteresEspeciais)

    senha = list(letras + numeros + especiais)
    shuffle(senha)

    return ''.join(senha)

def gerarPdfExames(exame, paciente, senha):
    pathTemplate = os.path.join(settings.BASE_DIR, 'templates/partials/senhaExame.html')
    templateRender = render_to_string(pathTemplate, {'exame': exame, 'paciente': paciente, 'senha': senha})

    path_output = BytesIO()

    HTML(string=templateRender).write_pdf(path_output)
    path_output.seek(0)

    return path_output