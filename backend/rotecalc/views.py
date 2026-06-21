from django.shortcuts import render #Conceito: recebo paramêtros da documentação, tais como, requisição, template e o contexto.
from django.http import HttpResponse 
# Create your views here.


#FUNÇÃO VIEW DO SITE, CONVERSANDO COM A FUNÇÕES QUE CRIEI
def corridas_app(request):
     if request.method == "POST":

        distancia = request.POST.get('distancia')
        consumo = request.POST.get('consumo')
        valor_corrida = request.POST.get('valor_corrida')
        preco_gasolina = request.POST.get('preco_gasolina')






#AO INVÉS UMA VARIAVEL PARA CADA ERRO DE CAMPO, CRIEI UM FOR ONDE O CONTEXT DO MESMO CASA COM O HTML
        for campo, valor in {"preco_gasolina":preco_gasolina, "distancia":distancia, "consumo":consumo, "valor_corrida":valor_corrida}.items():
            erro = validar_campo(valor)

            if erro:
                return render(request, 'ridecalc.html',
                context={"erro": erro,
                         "campo_erro":campo
                })





        #CONVERSANDO COM MINHA FUNÇÃO DE CALCULAR
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






#CRIANDO A FUNÇÃO QUE CALCULA TUDO
def calcular_corrida(distancia,consumo,valor_corrida, preco_gasolina):

    litros_gastos: float = float(distancia)/float(consumo)

    custo: float = litros_gastos * float(preco_gasolina)

    lucro: float = float(valor_corrida) - custo
    return(litros_gastos,custo,lucro)







#AQUI EU CRIEI UM TRATAMENTO PARA ERROS
def validar_campo(valor):

    if valor == None:
        return("O campo não pode ser vazio.")

    try:
        valor = float(valor)
        if valor <=0:
            return("O valor precisa ser maior que 0.")

    except ValueError:
        return("Valor inválido.")



