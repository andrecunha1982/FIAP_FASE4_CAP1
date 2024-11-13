
import oracledb
import pandas as pd

def conectar_oracle():
    try:
        conn = oracledb.connect(
            user="admin",
            password="FIAPfiap2024",
            dsn="fiap2024_low",
            config_dir=r"C:\Users\gabi_\Downloads\wallet",
            wallet_location=r"C:\Users\gabi_\Downloads\wallet",
            wallet_password="FIAPfiap2024"
        )
        print("Conexão com o Oracle estabelecida com sucesso!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao Oracle: {e}")
        return None

def criar_tabela(conn):
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT COUNT(*)
                FROM user_tables
                WHERE table_name = 'SENSORES'
            """)
            table_exists = cursor.fetchone()[0] > 0

            if table_exists:
                print("A tabela 'sensores' já existe. Limpando dados antigos.")
                cursor.execute("TRUNCATE TABLE sensores")
            else:
                create_table_sql = """
                CREATE TABLE sensores (
                    sensor_id INT PRIMARY KEY,
                    timestamp TIMESTAMP,
                    humidity FLOAT,
                    temperature FLOAT,
                    ph FLOAT,
                    phosphorus VARCHAR2(50),
                    potassium VARCHAR2(50),
                    irrigationOn NUMBER(1)
                )
                """
                cursor.execute(create_table_sql)
                print("Tabela criada com sucesso!")
        except oracledb.DatabaseError as e:
            print(f"Erro ao criar a tabela: {e}")
        finally:
            cursor.close()


def carregar_dados_csv(csv_path):
    df = pd.read_csv(csv_path, delimiter=';')
    print("Colunas no arquivo CSV:", df.columns)
    df['sensor_id'] = range(1, len(df) + 1)

    try:
        df['Timestamp'] = pd.to_datetime("2024-08-11 " + df['Timestamp'])
    except Exception as e:
        print(f"Erro ao converter a coluna 'Timestamp': {e}")

    return df


def inserir_dados_csv(conn, df):
    cursor = conn.cursor()
    for _, row in df.iterrows():
        try:
            cursor.execute(
                """
                INSERT INTO sensores (timestamp, temperature, humidity, ph, phosphorus, potassium, irrigationOn, sensor_id)
                VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
                """,
                (
                    row['Timestamp'],
                    float(row['Temperatura']),
                    float(row['Umidade']),
                    float(row['pH']),
                    str(row['Fósforo']),
                    str(row['Potássio']),
                    int(row['IrrigaçãoOn']),
                    row['sensor_id']
                )
            )
        except oracledb.DatabaseError as e:
            print(f"Erro ao inserir os dados do sensor_id {row['sensor_id']}: {e}")
    conn.commit()
    print("Dados inseridos com sucesso!")
    cursor.close()

def ler_dados(conn):
    cursor = conn.cursor()
    select_sql = "SELECT * FROM sensores"
    try:
        cursor.execute(select_sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except oracledb.DatabaseError as e:
        print(f"Erro ao ler os dados: {e}")
    finally:
        cursor.close()

def atualizar_dados(conn, sensor_id, new_humidity):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE sensores
            SET humidity = :1
            WHERE sensor_id = :2
            """,
            (new_humidity, sensor_id)
        )
        conn.commit()
        print(f"Dados do sensor_id {sensor_id} atualizados com sucesso!")
    except oracledb.DatabaseError as e:
        print(f"Erro ao atualizar os dados do sensor_id {sensor_id}: {e}")
    finally:
        cursor.close()

def excluir_dados(conn, sensor_id):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM sensores
            WHERE sensor_id = :1
            """,
            (sensor_id,)
        )
        conn.commit()
        print(f"Dados do sensor_id {sensor_id} excluídos com sucesso!")
    except oracledb.DatabaseError as e:
        print(f"Erro ao excluir os dados do sensor_id {sensor_id}: {e}")
    finally:
        cursor.close()


def main():
    conn = conectar_oracle()
    if conn:
        criar_tabela(conn)

        df = carregar_dados_csv(r"D:\FIAP\FIAP_FASE3\Arduino.csv")
        inserir_dados_csv(conn, df)

        # Ler dados
        print("Dados na tabela após inserção:")
        ler_dados(conn)

        # Testando a atualização de dados
        print("\nAtualizando dados do sensor_id 1...")
        atualizar_dados(conn, sensor_id=1, new_humidity=60.0)

        # Ler dados para verificar a atualização
        print("Dados na tabela após atualização:")
        ler_dados(conn)

        # Testando a exclusão de dados
        print("\nExcluindo dados do sensor_id 1...")
        excluir_dados(conn, sensor_id=1)

        # Ler dados para verificar a exclusão
        print("Dados na tabela após exclusão:")
        ler_dados(conn)

        conn.close()
        print("Conexão com o banco de dados encerrada.")

if __name__ == "__main__":
    main()
