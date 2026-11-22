import numpy as np
import pandas as pd

#Cálculo da matriz de transição
def matrizTransicao(novatos, p_permanencia):

    #Verifica se há novatos identificados no data frame
    if novatos.empty:
        raise ValueError("Não há novatos na base de dados!")

    if not 0 <= p_permanencia < 1:
        raise ValueError("A permanência deve estar entre 0 e 1!")

    respostas = (
        novatos["premium_sub_willingness"]
        .str.lower()
        .str.strip()
    )

    frequencias = respostas.value_counts(normalize=True)

    if not {"yes", "no"}.issubset(set(frequencias.index)):
        raise ValueError("A base precisa conter respostas Yes e No.")

    proporcao_yes = frequencias["yes"]
    proporcao_no = frequencias["no"]

    p11 = p_permanencia

    p12 = (1 - p11) * proporcao_yes
    p13 = (1 - p11) * proporcao_no

    matriz = np.array([
        [p11, p12, p13],
        [0,   1,   0],
        [0,   0,   1]
    ])

    print("\nMATRIZ DE TRANSIÇÃO P")
    print(matriz)
    print("\nSoma das linhas:")
    print(matriz.sum(axis=1))

    return matriz


#Calcula a matriz fundamental
def matrizFundamental(p):
    
    Q = p[:1, :1] #Primeira linha e primeira coluna.
    R = p[:1, 1:] #Primeira linha, a partir da segunda coluna.

    identidade = np.eye(Q.shape[0]) #Cria uma matriz identidade.

    N = np.linalg.inv(identidade - Q) #Calcula a inversa

    print("\nMATRIZ Q")
    print(Q)
    print("\nMATRIZ R")
    print(R)
    print("\nMATRIZ FUNDAMENTAL N")
    print(N)

    return N, R


#Calcula o tempo médio até a absorção
def calcularTempoAbsorcao(N):

    vetor_ones = np.ones((N.shape[0], 1))
    tempo = N @ vetor_ones 

    print("\nTEMPO MÉDIO ATÉ ABSORÇÃO")
    print(tempo)

    return tempo


#Probabilidades finais de absorção
#Implementação da fórmula B = N * R

def calcularProbabilidadeAbsorcao(N, R):

    B = N @ R

    print("\nPROBABILIDADES FINAIS DE ABSORÇÃO")
    print(B)
    print(f"\nProbabilidade de Premium: {B[0, 0]:.2%}")
    print(f"Probabilidade de Free Resistente: {B[0, 1]:.2%}")

    return B


def analisarSensibilidade(novatos):

    cenarios = [0.30, 0.50, 0.70, 0.90]
    resultados = []

    for p_permanencia in cenarios:
        P = matrizTransicao(
            novatos,
            p_permanencia
        )
        N, R = matrizFundamental(P)
        tempo = calcularTempoAbsorcao(N)
        B = calcularProbabilidadeAbsorcao(N, R)

        resultados.append({
            "Permanencia": p_permanencia,
            "Tempo medio": float(tempo[0, 0]),
            "Probabilidade Premium": float(B[0, 0]),
            "Probabilidade Resistente": float(B[0, 1])
        })

    return pd.DataFrame(resultados)
