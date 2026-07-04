from django.shortcuts import render, redirect #Conceito: recebo paramêtros da documentação, tais como, requisição, template e o contexto.
from django.http import HttpResponse # nem to usando isso, foi so pra testar as vezes, ele retorna uma pagina ao inves de template ate onde eu sei
from .models import Motorista, Corrida #Importando o motomoto
from django.contrib.auth import authenticate, login, logout # essa delicinha é do próprio django, parceiro dms
from django.contrib.auth.decorators import login_required
import re
# Create your views here.


#FUNÇÃO VIEW DO SITE, CONVERSANDO COM A FUNÇÕES QUE CRIEI

#=========================================VIEW CORRIDAS=========================================
@login_required
def corridas_app(request):
     if request.method == "POST":
        motorista = request.user
        distancia = request.POST.get('distancia')
        consumo = motorista.consumo
        valor_corrida = request.POST.get('valor_corrida')
        preco_gasolina = request.POST.get('preco_gasolina')

#->AO INVÉS DE UMA VARIAVEL PARA CADA ERRO DE CAMPO, CRIEI UM FOR ONDE O CONTEXT DO MESMO CASA COM O HTML
        for campo, valor in {"preco_gasolina":preco_gasolina, "distancia":distancia, "consumo":consumo, "valor_corrida":valor_corrida}.items():
            erro = validar_campo(valor)

            if erro:
                return render(request, 'ridecalc.html',
                context={"erro": erro,
                         "campo_erro":campo
                })


        #->CONVERSANDO COM MINHA FUNÇÃO DE CALCULAR
        litros_gastos, custo, lucro = calcular_corrida(distancia,consumo,valor_corrida, preco_gasolina)
        #AQUI EU TO SALVANDO NO BANCO OS DADOS DA CORRIDA
        corrida = Corrida(motorista=request.user,distancia=distancia, valor_corrida=valor_corrida, lucro=lucro)
        corrida.save()

        return render(request, 'ridecalc.html',
        context={
            "litros_gastos": litros_gastos,
            "custo": custo,
            "lucro": lucro,
            "valor_corrida": valor_corrida,
            "distancia": distancia,
        })
     elif request.method == "GET":
        return render(request, 'ridecalc.html')

#===========================<<<<<<<<<<<<<>>>>>>>>>>>>>>>>===============================================



#=================>>>>>>>>>>>>>VIEW CADASTRO<<<<<<<<<<<<=========================================

def cadastro_app(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        username = request.POST.get('email')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirma_senha')
        modelo = request.POST.get('modelo')
        consumo = request.POST.get('consumo')


#TRATANDO ERRO DE @ COM MASCARA NO CAMPO
        if not re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+", username):
            return render(request, 'cadastro.html', context={
                'erro_usuario': 'Digite um e-mail válido.'
            })

#TRATANDO CONFIRMAÇÃO DE SENHA BEM BASICAO
        if not senha or not confirma_senha:
            return render(request, 'cadastro.html', context={
            "erro_senha": "Preencha todos os campos de senha."
            })

        if senha != confirma_senha:
            erro_senha = "Senha não confere."
            return render(request, 'cadastro.html', context={
                "erro_senha" : erro_senha
                })
        #TESTANDO SE UM USUARIO JA EXISTE - USANDO ORM DJANGO PURO MT BRABO🔥🔥🔥🔥
        if Motorista.objects.filter(username=username).exists():
            erro_usuario = "Email já cadastrado."
            return render(request, 'cadastro.html', context={'erro_usuario':erro_usuario})
        
        #AQUI EU TO SALVANDO NO BANCO DADOS, O REDIRECT É PRO USUARIO JA VOLTAR PRA TELA LOGIN
        motorista = Motorista(first_name=nome,username=username,modelo=modelo, password=senha,consumo=consumo, email=username)
        motorista.set_password(senha)
        motorista.save()
        return redirect('login_app')
    elif request.method=="GET":
        return render(request, 'cadastro.html')


#===========================================<<<<<<<>>>>>>>>>>=====================================================



#========================================VIEW LOGIN=================================

def login_app(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        senha = request.POST.get('senha')
        usuario = authenticate(request,username=username,password=senha)
    #ESTOU TRATANDO O ERRO DO USUARIO NAO EXISTIR:
        if usuario:
            login(request, usuario)
            return redirect('corridas_app')
        else:
            erro_login="Usuário não encontrado."
            return render(request,'login.html',context={"erro_login":erro_login})
    elif request.method == 'GET':
        return render(request, 'login.html')
#=================================================================================

#===================================VIEW LOGOUT===============================
@login_required
def logout_app(request):
    if request.method == "POST":
        logout(request)
        return redirect('login_app')

#=======================================================================

#===================================VIEW PERFIL========================

@login_required
def perfil_app(request):
    motorista = request.user
    if request.method == "POST":
        modelo = request.POST.get("modelo")
        consumo = request.POST.get("consumo")

        if consumo:
            erro = validar_campo(consumo)
            if erro:
                return render(request, "perfil.html", context={
                    "motorista": motorista,
                    "erro": erro,
                    "campo_erro": "consumo"
                })
            motorista.consumo = consumo

        if modelo:
            motorista.modelo = modelo

        motorista.save()
        return redirect("perfil_app")

    return render(request, "perfil.html", context={
        "motorista": motorista
    })


#=====================================VIEW HISTORICO==============================
@login_required
def historico_app(request):
    if request.method == 'GET':
        motorista = request.user
        corridas = Corrida.objects.filter(motorista=motorista).order_by('-data')
        resultado = calcular_metricas(motorista)
        return render(request, 'historico.html', context={
        "lucro_total" : resultado["lucro_total"],
        "distancia_total" : resultado["distancia_total"],
        "soma_corridas" : resultado["soma_corridas"],
        "total_corridas": resultado["total_corridas"],
        "media_corridas": resultado["media_corridas"],
        "corridas" : corridas,
        })
#==================================================================================


#=========================FUNÇÕES DO APP================================>
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

#CRIANDO A FUNÇÃO QUE CALCULA TUDO
#=========================================================================>
def calcular_corrida(distancia,consumo,valor_corrida, preco_gasolina):      

    litros_gastos: float = float(distancia)/float(consumo)

    custo: float = litros_gastos * float(preco_gasolina)

    lucro: float = float(valor_corrida) - custo
    return(litros_gastos,custo,lucro)
#========================================================================>

#FUNÇÃO QUE CALCULA AS MÉTRICAS PEGANDO DO BANCO DE DADOS
def calcular_metricas(motorista):
    #calculando métricas através de um for básico
    corridas = Corrida.objects.filter(motorista=motorista)
    lucro_total = 0
    distancia_total = 0
    soma_corridas = 0
    media_corridas = 0
    for corrida in corridas:
        lucro_total += corrida.lucro
        distancia_total += corrida.distancia
        soma_corridas += corrida.valor_corrida

    total_corridas = corridas.count()
    #to tratando o erro no caso do total de corridas for igual 0
    if total_corridas > 0:
        media_corridas = soma_corridas / total_corridas
    return{
        "lucro_total" : lucro_total,
        "distancia_total" : distancia_total,
        "soma_corridas" : soma_corridas,
        "total_corridas": total_corridas,
        "media_corridas": media_corridas,
    }
#=========================<<<<<<<<<>>>>>>>>>>>==========================   


#AQUI EU CRIEI UM TRATAMENTO PARA ERROS
#======================================================>
def validar_campo(valor):
    try:
        valor = float(valor)
        if valor <=0:
            return("O valor precisa ser maior que 0.")

    except ValueError:
        return("Valor inválido.")
#=======================================================>
