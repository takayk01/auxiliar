
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

