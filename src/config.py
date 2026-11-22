from pathlib import Path #Para manipulção de caminhos de arquivos

#Definição dos diretórios

#Diretório absoluto da raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent 

#Diretório da base de dados
DATA_PATH = BASE_DIR /"data"/"Spotify_data.xlsx"

#Diretório dos resultados
OUTPUT_DIR = BASE_DIR/"outputs"

#Cria a pasta outputs caso ela não exista
OUTPUT_DIR.mkdir(parents = True, exist_ok = True)

#Definição dos estados da cadeia de Markov
FREE_NOVATO = "Free Novato"
PREMIUM = "Premium"
FREE_RESISTENTE = "Free Resistente"

ESTADOS = [
    FREE_NOVATO,
    PREMIUM,
    FREE_RESISTENTE
]

