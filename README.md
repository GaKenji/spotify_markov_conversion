# Spotify Markov Conversion

Projeto acadêmico desenvolvido em Python para analisar o comportamento de usuários do Spotify e estudar sua possível migração entre planos de assinatura por meio de **Cadeias de Markov Absorventes**.

A partir de uma base de dados de comportamento de usuários, o projeto utiliza conceitos de probabilidade e álgebra linear para construir uma matriz de transição, calcular probabilidades de absorção e estimar o tempo médio até que os usuários alcancem um dos estados finais definidos no modelo.

O projeto também contempla análises complementares de segmentação de perfis e simulação estocástica.

## Objetivos

- Explorar os dados de comportamento e assinatura dos usuários.
- Construir um modelo de Cadeia de Markov para representar possíveis transições entre estados.
- Calcular a matriz fundamental e as probabilidades de absorção.
- Estimar o tempo médio até a absorção.
- Investigar diferenças entre perfis de usuários por meio de segmentação.
- Validar os resultados teóricos por simulação de Monte Carlo.
- Interpretar os resultados sob uma perspectiva de negócio.

## Fonte dos dados

A base utilizada neste projeto é o **Spotify User Behavior Dataset**, disponibilizado no Kaggle:

[Spotify User Behavior Dataset — Kaggle](https://www.kaggle.com/datasets/meeraajayakumar/spotify-user-behavior-dataset)

O conjunto de dados contém respostas de questionário relacionadas aos hábitos de utilização do Spotify, preferências musicais, consumo de podcasts e planos de assinatura.

Entre as variáveis utilizadas estão:

| Variável | Descrição no projeto |
|---|---|
| `spotify_subscription_plan` | Plano de assinatura do usuário |
| `spotify_usage_period` | Tempo de utilização do Spotify |
| `premium_sub_willingness` | Intenção declarada de assinar o Premium |
| `pod_lis_frequency` | Frequência de consumo de podcasts |
| `music_recc_rating` | Avaliação das recomendações musicais |

**Importante:** a base representa respostas de questionário, e não um histórico longitudinal de transições reais dos usuários. Portanto, as probabilidades calculadas são resultados de um modelo construído sob hipóteses, e não taxas de conversão efetivamente observadas pelo Spotify.

Consulte a licença indicada na página original do Kaggle antes de redistribuir o arquivo de dados.

## Metodologia — Cadeia de Markov

### 1. Exploração e preparação dos dados

A base foi carregada e analisada utilizando Pandas. Foram examinadas as frequências dos planos de assinatura, a disposição para assinar o Premium e o tempo de utilização do serviço.

Na implementação atual, foram identificados:

- 520 registros na base;
- 424 usuários no plano Free;
- 96 usuários no plano Premium;
- 84 usuários classificados como Free Novatos.

Para a análise principal, foram selecionados usuários que utilizam o plano gratuito e possuem menos de seis meses de utilização.

### 2. Definição dos estados

A implementação atual utiliza três estados:

| Estado | Classificação | Significado no modelo |
|---|---|---|
| Free Novato | Transitório | Usuário gratuito com menos de seis meses de utilização |
| Premium | Absorvente | Usuário que migrou para o plano Premium |
| Free Resistente | Absorvente | Usuário sem intenção declarada de assinar o Premium |

A classificação de Free Resistente utiliza a resposta negativa à intenção de assinatura como aproximação comportamental. Considerá-lo absorvente é uma hipótese simplificadora do modelo, não uma comprovação de que o usuário nunca assinará o Premium.

### 3. Matriz de transição

A matriz foi construída considerando uma probabilidade hipotética de permanência de 70% no estado Free Novato.

As respostas dos usuários foram utilizadas para distribuir os 30% restantes entre os estados Premium e Free Resistente, proporcionalmente às respostas positivas e negativas sobre a intenção de assinatura.

A matriz obtida foi:

\[
P =
\begin{bmatrix}
0,70 & 0,03928571 & 0,26071429 \\
0 & 1 & 0 \\
0 & 0 & 1
\end{bmatrix}
\]

Cada linha representa um estado de origem e cada coluna representa um estado de destino. A soma das probabilidades de cada linha é igual a 1.

**Atenção:** os 70% de permanência são uma hipótese utilizada na modelagem e não uma frequência observada diretamente na base.

### 4. Matriz fundamental

Para analisar a cadeia absorvente, a matriz de transição é decomposta em:

\[
P =
\begin{bmatrix}
Q & R \\
0 & I
\end{bmatrix}
\]

A matriz fundamental é calculada por:

\[
N = (I-Q)^{-1}
\]

No modelo implementado:

\[
N = [3,3333]
\]

Esse resultado representa aproximadamente 3,33 visitas esperadas ao estado transitório, incluindo a visita inicial, antes da absorção.

### 5. Probabilidades de absorção

As probabilidades finais de absorção são calculadas por:

\[
B = N \cdot R
\]

Resultados obtidos:

| Estado absorvente | Probabilidade |
|---|---:|
| Premium | 13,10% |
| Free Resistente | 86,90% |

Esses valores representam as probabilidades eventuais de absorção no modelo, considerando as hipóteses adotadas.

### 6. Análise de sensibilidade

Foram avaliados quatro cenários hipotéticos de permanência no estado Free Novato:

| Permanência | Tempo médio até absorção | Premium | Free Resistente |
|---:|---:|---:|---:|
| 30% | 1,43 | 13,10% | 86,90% |
| 50% | 2,00 | 13,10% | 86,90% |
| 70% | 3,33 | 13,10% | 86,90% |
| 90% | 10,00 | 13,10% | 86,90% |

A análise demonstra que, mantendo a proporção dos destinos de saída, a probabilidade de absorção permanece constante. A alteração da permanência modifica o tempo esperado até a absorção.

## Análises complementares

### Segmentação de perfis

Esta etapa tem como objetivo investigar se diferentes perfis comportamentais apresentam distintas proporções de intenção de assinatura Premium.

A proposta é utilizar a variável `pod_lis_frequency` para comparar grupos de usuários com diferentes frequências de consumo de podcasts.

O integrante responsável deverá:

1. Definir grupos de comparação com base na frequência de consumo de podcasts.
2. Aplicar os filtros à base de dados.
3. Identificar os usuários Free Novatos de cada grupo.
4. Calcular as proporções de respostas positivas e negativas sobre a intenção de assinar o Premium.
5. Construir uma matriz de transição para cada grupo, mantendo a mesma hipótese de permanência de 70% para permitir a comparação.
6. Calcular as respectivas matrizes fundamentais e probabilidades de absorção.
7. Apresentar uma tabela comparativa e interpretar as diferenças encontradas.

A análise deverá deixar claro que os resultados representam diferenças de intenção declarada entre os grupos, e não conversões efetivamente observadas.

**Responsável:** [Nome do desenvolvedor responsável pela segmentação]

### Simulação de Monte Carlo

Esta etapa tem como objetivo validar computacionalmente os resultados obtidos pela álgebra linear.

O integrante responsável deverá:

1. Simular 10.000 usuários percorrendo a cadeia de Markov.
2. Utilizar a matriz de transição principal como base para as transições.
3. Registrar a evolução da quantidade de usuários em cada estado ao longo dos ciclos.
4. Comparar as probabilidades finais simuladas com os valores teóricos calculados por \(B=N\cdot R\).
5. Apresentar gráficos de evolução e uma comparação entre resultados teóricos e simulados.

**Responsável:** [Nome do desenvolvedor responsável pela simulação]

## Tecnologias utilizadas

- **Python:** linguagem principal do projeto.
- **Pandas:** carregamento, filtragem e análise dos dados.
- **NumPy:** operações matriciais e cálculos de álgebra linear.
- **Matplotlib:** geração de gráficos.
- **Seaborn:** visualização da matriz de transição.
- **NetworkX:** construção e representação do grafo de estados.

## Estrutura do projeto

```text
spotify-markov-conversion/
│
├── data/
│   └── Spotify_data.csv
│
├── outputs/
│   ├── matriz_transicao.png
│   └── grafo_transicao_completo.png
│
├── src/
│   ├── main.py
│   ├── carregar_dados.py
│   ├── analisar_frequencias.py
│   ├── free_novatos.py
│   ├── matrizes_e_probabilidades.py
│   └── visualizacao.py
│
├── analises/
│   ├── segmentacao.py
│   └── monte_carlo.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

Os módulos `segmentacao.py` e `monte_carlo.py` correspondem às análises complementares e poderão ser adicionados conforme o desenvolvimento dessas etapas.

## Como executar

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd spotify-markov-conversion
```

### 2. Criar o ambiente virtual

```bash
python -m venv .venv
```

### 3. Ativar o ambiente virtual

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Disponibilizar a base de dados

Baixe o arquivo disponibilizado no Kaggle e coloque-o na pasta `data/`, respeitando o nome e o formato esperados pelo módulo `carregar_dados.py`.

### 6. Executar a análise principal

```bash
python src/main.py
```

Os resultados e as visualizações serão apresentados no terminal e os gráficos serão salvos na pasta `outputs/`.

## Limitações do modelo

- A base utilizada é transversal e não acompanha a evolução dos mesmos usuários ao longo do tempo.
- A probabilidade de permanência de 70% foi definida como hipótese de modelagem.
- A intenção declarada de assinatura não representa necessariamente uma conversão real.
- O estado Free Resistente é uma simplificação baseada na resposta negativa à intenção de assinatura.
- O modelo assume probabilidades de transição constantes ao longo dos ciclos.
- Os resultados dependem das hipóteses utilizadas na construção da matriz de transição.

Portanto, as probabilidades calculadas devem ser interpretadas como resultados do modelo proposto, e não como previsões oficiais ou taxas reais de conversão do Spotify.

## Desenvolvedores e contribuições

### Parte 1 — Construção matemática e implementação da cadeia

Responsável pela exploração da base, identificação dos usuários Free Novatos, construção da matriz de transição, decomposição em matrizes \(Q\) e \(R\), cálculo da matriz fundamental, tempo médio até absorção, probabilidades finais, análise de sensibilidade e geração das visualizações.

**Desenvolvedor:** [Gabriel Kenji Do Martins]


### Parte 2 — Segmentação de perfis e análise complementar

Responsável pela segmentação dos usuários, comparação entre perfis comportamentais e interpretação das diferenças nas probabilidades de absorção.

**Desenvolvedor:** [Lana Cristina Da Silva Bastos]

---

Projeto desenvolvido para fins acadêmicos, com foco na aplicação de Cadeias de Markov, álgebra linear, análise de dados e simulação computacional.
