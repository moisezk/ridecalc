from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
#DECLARANDO A CONSTANTE DO VALOR DA GASOLINA
preco_gasolina = 5.80



def corridas_app(request):
     if request.method == "POST":
        distancia = request.POST.get('distancia')
        consumo = request.POST.get('consumo')
        valor_corrida = request.POST.get('valor_corrida')
        litros_gastos, custo, lucro = calcular_corrida(distancia,consumo,valor_corrida)
        return render(request, 'corridas.html',
        context={
            "litros_gastos": litros_gastos,
            "custo": custo,
            "lucro": lucro
        })
     elif request.method == "GET":
        return render(request, 'corridas.html')


#CRIANDO A FUNÇÃO QUE CALCULA TUDO
def calcular_corrida(distancia,consumo,valor_corrida):
    litros_gastos = float(distancia)/float(consumo)
    custo = litros_gastos * preco_gasolina
    lucro = float(valor_corrida) - custo
    return(litros_gastos,custo,lucro)