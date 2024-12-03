import oracledb
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

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
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except oracledb.DatabaseError as e:
        print(f"Erro ao ler os dados: {e}")
    finally:
        cursor.close()


# Função principal
def main():
    conn = conectar_oracle()
    if conn:
        ler_dados(conn)

        conn.close()
        print("Conexão com o banco de dados encerrada.")


if __name__ == "__main__":
    main()