import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

from config import ESTADOS, FREE_NOVATO, FREE_RESISTENTE, PREMIUM, OUTPUT_DIR

#Desenha o grafo que representa as transições entre os estados 
def desenharGrafo(P):

    G = nx.DiGraph()#Cria um grafo direcionado. As transições possuem origem e destino
    G.add_nodes_from(ESTADOS)

    for i, origem in enumerate(ESTADOS):
        for j, destino in enumerate(ESTADOS):

            probabilidade = P[i, j]
            if probabilidade > 0:
                G.add_edge(
                    origem,
                    destino,
                    weight=probabilidade #Armazena a probabilidade de cada transição
                )

    posicoes = {
        FREE_NOVATO: (0, 1),
        PREMIUM: (-1, 0),
        FREE_RESISTENTE: (1, 0)
    }

    plt.figure(figsize=(10, 7))
    nx.draw_networkx_nodes(
        G,
        posicoes,
        node_size=3500
    )
    nx.draw_networkx_labels(
        G,
        posicoes,
        font_size=10,
        font_weight="bold"
    )
    nx.draw_networkx_edges(
        G,
        posicoes,
        arrows=True,
        arrowsize=25,
        connectionstyle="arc3,rad=0.15"
    )

    rotulos = {
        (origem, destino): f"{dados['weight']:.2%}"
        for origem, destino, dados in G.edges(data=True)
    }

    nx.draw_networkx_edge_labels(
        G,
        posicoes,
        edge_labels=rotulos,
        font_size=9
    )

    plt.title("Grafo de Transição - Cadeia de Markov Spotify")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "grafo_transicao.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()



#Visualizando a matriz de transição
def visualizarMatriz(P):

    plt.figure(figsize=(8, 6))

    sns.heatmap(
        P,
        annot=True,#Exibe os valores dentro das células.
        fmt=".3f",
        cmap="Blues",
        xticklabels=ESTADOS,
        yticklabels=ESTADOS,
        vmin=0,
        vmax=1
    )

    plt.title("Matriz de Transição P")
    plt.xlabel("Estado de destino")
    plt.ylabel("Estado de origem")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "matriz_transicao.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()