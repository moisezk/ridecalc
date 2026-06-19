from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


#FUNÇÃO VIEW DO SITE, CONVERSANDO COM A FUNÇÕES QUE CRIEI
def corridas_app(request):
     if request.method == "POST":
        distancia = request.POST.get('distancia')
        consumo = request.POST.get('consumo')
        valor_corrida = request.POST.get('valor_corrida')
        preco_gasolina = request.POST.get('preco_gasolina')
        litros_gastos, custo, lucro = calcular_corrida(distancia,consumo,valor_corrida, preco_gasolina)
        return render(request, 'ridecalc.html',
        context={
            "litros_gastos": litros_gastos,
            "custo": custo,
            "lucro": lucro,
            "valor_corrida": valor_corrida,
            "distancia": distancia
        })
     elif request.method == "GET":
        return render(request, 'ridecalc.html')


#CRIANDO A FUNÇÃO QUE CALCULA TUDO
def calcular_corrida(distancia,consumo,valor_corrida, preco_gasolina):
    litros_gastos: float = float(distancia)/float(consumo)
    custo: float = litros_gastos * float(preco_gasolina)
    lucro: float = float(valor_corrida) - custo
    return(litros_gastos,custo,lucro)