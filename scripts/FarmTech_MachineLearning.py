import oracledb
import pandas as pd

# Conexão com o Oracle
def conectar_oracle():
    try:
        conn = oracledb.connect(
            user="admin",
            password="FIAPfiap2024",
            dsn="fiap2024_low",
            config_dir=r"C:\opt\OracleCloud\MYDB",
            wallet_location=r"C:\opt\OracleCloud\MYDB",
            wallet_password="FIAPfiap2024"
        )
        print("Conexão com o Oracle estabelecida com sucesso!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao Oracle: {e}")
        return None

# Funções de manipulação dos dados
def ler_dados(conn):
    cursor = conn.cursor()
    select_sql = "SELECT * FROM FASE04_SENSORES"
    try:
        cursor.execute(select_sql)
        # Coletando os dados e os nomes das colunas
        columns = [desc[0] for desc in cursor.description]  # Nome das colunas
        rows = cursor.fetchall()
        # Criando o DataFrame
        df = pd.DataFrame(rows, columns=columns)
        return df
    except oracledb.DatabaseError as e:
        print(f"Erro ao ler os dados: {e}")
        return None
    finally:
        cursor.close()

# Função principal
def main():
    conn = conectar_oracle()
    if conn:
        df = ler_dados(conn)
        if df is not None:
            print("Dados carregados com sucesso no DataFrame!")
            print(df)  # Exibe o DataFrame
        conn.close()
        print("Conexão com o banco de dados encerrada.")

if __name__ == "__main__":
    main()
