from carregar_dados import carregarDados
from analisar_frequencias import analisarFrequencias
from free_novatos import identificarFreeNovatos
import matrizes_e_probabilidades as mp
import visualizacao as vz

df = carregarDados()#Carrega a base de dados
frequencias = analisarFrequencias(df)#Realiza uma análise de frequências
novatos = identificarFreeNovatos(df)#Identifica usuários novatos com pouco tempo de uso
resultados = mp.analisarSensibilidade(novatos)#Análise de sendibilidade para deduzir um p_permanencia = p11 da matriz de transição

print("\nANÁLISE DE SENSIBILIDADE")
print(resultados.to_string(index=False))

#Probabilidade de um usuário que está no estado Free Novato continuar nesse mesmo estado no próximo ciclo (semestre).
p_permanencia = 0.7 #70% como hipótese de simulação

if p_permanencia is None:
    raise ValueError("Atribua um valor justificado a p_permanencia")

#Constrói a matriz de transição
p = mp.matrizTransicao(novatos, p_permanencia)

#Calcula a Matriz Fundamental
N, R = mp.matrizFundamental(p)

#Calcular tempo médio
tempo = mp.calcularTempoAbsorcao(N)

#Calcula probabilidades de absorção
B = mp.calcularProbabilidadeAbsorcao(N, R)

#Gerar representação vizual de transição entre os estados e a matriz de transição
vz.desenharGrafo(p)
vz.visualizarMatriz(p)
print("\nAnálise finalizada!")
