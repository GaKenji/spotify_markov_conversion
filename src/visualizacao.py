import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path as MplPath
import seaborn as sns

from config import ESTADOS, OUTPUT_DIR

#Desenha o grafo que representa as transições entre os estados 

def desenharGrafo(matriz):

    estados = ESTADOS
    G = nx.DiGraph()

    # Criar estados e transições
    for estado in estados:
        G.add_node(estado)

    for i, origem in enumerate(estados):
        for j, destino in enumerate(estados):
            probabilidade = matriz[i][j]

            if probabilidade > 0:
                G.add_edge(origem, destino, weight=probabilidade)

    # Posição dos estados
    pos = {
        "Free Novato": (0, 1.5),
        "Premium": (-1.5, -1),
        "Free Resistente": (1.5, -1)
    }

    fig, ax = plt.subplots(figsize=(12, 9))

    # Separar transições e autotransições
    lacos = [(u, v) for u, v in G.edges() if u == v]
    transicoes = [(u, v) for u, v in G.edges() if u != v]

    # Desenhar transições entre estados diferentes
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=transicoes,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=25,
        width=2,
        connectionstyle="arc3,rad=0.12",
        min_source_margin=20,
        min_target_margin=20,
        ax=ax
    )

    # Definir manualmente os caminhos dos três laços
    configuracao_lacos = {

        "Free Novato": {
            "pontos": [
                (-0.12, 1.73),
                (-0.42, 2.12),
                (0.42, 2.12),
                (0.12, 1.73)
            ],
            "rotulo": (0, 2.16)
        },

        "Premium": {
            "pontos": [
                (-1.73, -0.88),
                (-2.12, -0.72),
                (-2.12, -1.28),
                (-1.73, -1.12)
            ],
            "rotulo": (-2.12, -1.00)
        },

        "Free Resistente": {
            "pontos": [
                (1.73, -1.12),
                (2.12, -1.28),
                (2.12, -0.72),
                (1.73, -0.88)
            ],
            "rotulo": (2.12, -1.00)
        }
    }

    # Desenhar os laços com curvas Bézier
    for estado in estados:
        config = configuracao_lacos[estado]
        caminho = MplPath(
            config["pontos"],
            [
                MplPath.MOVETO,
                MplPath.CURVE4,
                MplPath.CURVE4,
                MplPath.CURVE4
            ]
        )

        seta = FancyArrowPatch(
            path=caminho,
            arrowstyle="-|>",
            mutation_scale=20,
            linewidth=2,
            color="black",
            zorder=2
        )

        ax.add_patch(seta)

        # Exibir probabilidade da autotransição
        probabilidade = G[estado][estado]["weight"]
        x, y = config["rotulo"]
        ax.text(
            x,
            y,
            f"{probabilidade:.2%}",
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold",
            bbox=dict(
                facecolor="white",
                edgecolor="none",
                pad=2
            ),
            zorder=4
        )

    # Desenhar os nós depois das setas
    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=3000,
        node_color="steelblue",
        edgecolors="black",
        linewidths=1.2,
        ax=ax
    )
    nx.draw_networkx_labels(
        G,
        pos,
        font_size=10,
        font_weight="bold",
        ax=ax
    )

    # Rótulos das transições entre estados diferentes
    rotulos = {
        (origem, destino): f"{dados['weight']:.2%}"
        for origem, destino, dados in G.edges(data=True)
        if origem != destino
    }
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=rotulos,
        font_size=11,
        rotate=False,
        label_pos=0.5,
        ax=ax
    )
    ax.set_title(
        "Grafo de Transição - Cadeia de Markov Spotify",
        fontsize=15,
        pad=25
    )
    ax.set_xlim(-2.8, 2.8)
    ax.set_ylim(-2.0, 2.8)
    ax.axis("off")

    plt.tight_layout()
    plt.savefig(
        "outputs/grafo_transicao_completo.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()
    plt.close()




#Visualizando a matriz de transição
def visualizarMatriz(P):

    plt.figure(figsize=(8, 6))

    sns.heatmap(
        P,
        annot=True,#Exibe os valores dentro das células.
        fmt=".3f",
        cmap="Greens",
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