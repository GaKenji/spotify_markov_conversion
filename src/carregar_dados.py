import pandas as pd

from config import DATA_PATH

def carregarDados():

    #Verifica a existência do arquivo
    if not DATA_PATH.exists():
        #Se não existir, a execução é interrompida e o erro é exibido
        raise FileNotFoundError(f"Arquivo não encontrado: {DATA_PATH}")

    df = pd.read_excel(DATA_PATH)

    # Remove espaços extras dos nomes das colunas.
    df.columns = df.columns.str.strip()

    # Remove espaços extras dos valores textuais.
    for coluna in df.select_dtypes(include="object").columns:
        df[coluna] = df[coluna].str.strip()

    print("Base de dados carregada com sucesso!")
    print(f"Quantidade de registros: {len(df)}")

    return df