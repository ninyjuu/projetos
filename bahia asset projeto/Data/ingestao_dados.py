import pandas as pd
import pyodbc
import datetime

NOME_ARQUIVO = 'input.csv' 
SERVER = '.\SQLEXPRESS' 
DATABASE = 'DBDesafioFullstack'
ODBC_DRIVER = '{ODBC Driver 17 for SQL Server}' 

CONN_STRING = (
    f'DRIVER={ODBC_DRIVER};'
    f'SERVER={SERVER};'
    f'DATABASE={DATABASE};'
    f'Trusted_Connection=yes;' 
)

def ingere_dados():
    cnxn = None
    try:
        df = pd.read_csv(NOME_ARQUIVO, sep=';', encoding='utf-8-sig') 
        print(f"Arquivo '{NOME_ARQUIVO}' lido. Total de {len(df)} linhas.")

        df.columns = df.columns.str.strip() 
        
        # 1. CORREÇÃO: Trata a data
        df['Data_Trade'] = pd.to_datetime(df['Data_Trade'], dayfirst=True).dt.strftime('%Y-%m-%d')
        
        # 2. CORREÇÃO: Trata os separadores decimais (Troca ',' por '.') e converte para float
        df['Quantidade'] = df['Quantidade'].astype(str).str.replace(',', '.', regex=False)
        df['Emolumento'] = df['Emolumento'].astype(str).str.replace(',', '.', regex=False)
        
        # Remove linhas com valores nulos (que podem causar erro na conversão)
        df.dropna(subset=['Quantidade', 'Emolumento'], inplace=True)
        
        # Converte para float (número decimal)
        df['Quantidade'] = df['Quantidade'].astype(float)
        df['Emolumento'] = df['Emolumento'].astype(float)
        
        cnxn = pyodbc.connect(CONN_STRING)
        cursor = cnxn.cursor()
        print("Conexão com SQL Server estabelecida.")

        sql_insert = """
            INSERT INTO Ordem (Data_Trade, Ativo, Quantidade, Emolumento)
            VALUES (?, ?, ?, ?)
        """
        
        dados_para_inserir = df[[
            'Data_Trade', 
            'Ativo', 
            'Quantidade', 
            'Emolumento' 
        ]].values.tolist()

        cursor.executemany(sql_insert, dados_para_inserir)
        cnxn.commit() 
        print(f"\n{len(dados_para_inserir)} ordens inseridas com sucesso na tabela Ordem.")

    except pyodbc.Error as ex:
        if cnxn:
            cnxn.rollback()
        print(f"ERRO SQL/Conexão: {ex.args[1]}")
    except Exception as e:
        print(f"ERRO: {e}")
    finally:
        if cnxn:
            cnxn.close()
            print("Conexão fechada.")


if __name__ == "__main__":
    ingere_dados()