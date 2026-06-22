from django.shortcuts import render, redirect #Conceito: recebo paramêtros da documentação, tais como, requisição, template e o contexto.
from django.http import HttpResponse # nem to usando isso, foi so pra testar as vezes, ele retorna uma pagina ao inves de template ate onde eu sei
from .models import Motorista #Importando o motomoto
from django.contrib.auth import authenticate, login # essa delicinha é do próprio django, parceiro dms
# Create your views here.


#FUNÇÃO VIEW DO SITE, CONVERSANDO COM A FUNÇÕES QUE CRIEI

#=========================================VIEW CORRIDAS=========================================
def corridas_app(request):
     if request.method == "POST":

        distancia = request.POST.get('distancia')
        consumo = request.POST.get('consumo')
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

#TRATANDO CONFIRMAÇÃO DE SENHA BEM BASICAO
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



#AQUI EU CRIEI UM TRATAMENTO PARA ERROS
#======================================================>
def validar_campo(valor):

    if valor == None:
        return("O campo não pode ser vazio.")

    try:
        valor = float(valor)
        if valor <=0:
            return("O valor precisa ser maior que 0.")

    except ValueError:
        return("Valor inválido.")
#=======================================================>
