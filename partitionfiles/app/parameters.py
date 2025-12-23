
import pandas as pd
import base64

# Funções
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    
def limpar_df(df):
    df = df.fillna("")
    df = df.replace('nan', '')
    df = df.astype(str)
    return df

def ler_arquivo(path, encoding='utf-8-sig'):    
    df = pd.read_csv(
                path,
                sep=";",           
                encoding=encoding, 
                dtype=str,         
            )
    
    df = limpar_df(df)    
    return df

def partition_files(df, max_rows):
    def save_file(partes, contador):
        df_saida = pd.concat(partes)
        nome_arquivo_part = f'{nome_arquivo}_part_{contador}.csv'
        csv_valid_sap = df_saida.to_csv( index=False, sep=";", encoding="utf-8-sig" )
        dict_csv = {}
        dict_csv["arq"]  = csv_valid_sap
        dict_csv["nome"] = nome_arquivo_part
        return dict_csv
        
    nome_arquivo   = 'clientes_tel_validos'
    coluna_cliente = 'cliente'
    linhas_maximas = max_rows
    
    df     = df.sort_values(by=coluna_cliente)
    grupos = df.groupby(coluna_cliente)

    # Inicialização
    contador_arquivo = 1
    linhas_atuais    = 0
    partes           = []
    files            = []
    
    # Itera pelos grupos
    for cliente, grupo in grupos:
        qtd_linhas = len(grupo)
        
        # Se adicionar esse grupo ultrapassar o limite, salva o atual e começa novo
        if linhas_atuais + qtd_linhas > linhas_maximas:
            dict_csv = save_file(partes, contador_arquivo)
            files.append(dict_csv)
            
            # Reset
            contador_arquivo += 1
            partes = []
            linhas_atuais = 0
        
        # Adiciona o grupo atual
        partes.append(grupo)
        linhas_atuais += qtd_linhas

    # Salva o último arquivo restante
    if partes:        
        dict_csv = save_file(partes, contador_arquivo)
        files.append(dict_csv)
        
    return files

