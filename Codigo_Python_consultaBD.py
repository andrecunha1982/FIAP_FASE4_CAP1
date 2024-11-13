import oracledb
import pandas as pd
import matplotlib.pyplot as plt


# Conexão com o Oracle
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


# Criar tabela
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


# Carregar dados do CSV
def carregar_dados_csv(csv_path):
    df = pd.read_csv(csv_path, delimiter=';')
    print("Colunas no arquivo CSV:", df.columns)
    df['sensor_id'] = range(1, len(df) + 1)

    # Convertendo a coluna 'Timestamp' para datetime
    try:
        df['Timestamp'] = pd.to_datetime("2024-08-11 " + df['Timestamp'])
    except Exception as e:
        print(f"Erro ao converter a coluna 'Timestamp': {e}")

    # Substituindo "NAO" por 0 e "SIM" por 1 nas colunas de pH, Fósforo e Potássio
    df['pH'] = df['pH'].replace({"NAO": 0, "SIM": 1}).astype(float)
    df['Fósforo'] = df['Fósforo'].replace({"NAO": 0, "SIM": 1}).astype(int)
    df['Potássio'] = df['Potássio'].replace({"NAO": 0, "SIM": 1}).astype(int)
    return df


# Inserir dados no banco de dados
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


# Funções de manipulação dos dados
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


# Função para gerar o dashboard
def gerar_dashboard(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT timestamp, temperature, humidity, ph FROM sensores")
        data = cursor.fetchall()

        timestamps = [row[0] for row in data]
        temperatures = [row[1] for row in data]
        humidities = [row[2] for row in data]
        ph_values = [row[3] for row in data]

        plt.figure(figsize=(12, 8))

        # Gráfico de Temperatura
        plt.subplot(3, 1, 1)
        plt.plot(timestamps, temperatures, color='r')
        plt.title('Temperatura ao longo do tempo')
        plt.xlabel('Timestamp')
        plt.ylabel('Temperatura')

        # Gráfico de Umidade
        plt.subplot(3, 1, 2)
        plt.plot(timestamps, humidities, color='b')
        plt.title('Umidade ao longo do tempo')
        plt.xlabel('Timestamp')
        plt.ylabel('Umidade')

        # Gráfico de pH
        plt.subplot(3, 1, 3)
        plt.plot(timestamps, ph_values, color='g')
        plt.title('pH ao longo do tempo')
        plt.xlabel('Timestamp')
        plt.ylabel('pH')

        plt.tight_layout()
        plt.show()

    except oracledb.DatabaseError as e:
        print(f"Erro ao gerar o dashboard: {e}")
    finally:
        cursor.close()


# Função principal
def main():
    conn = conectar_oracle()
    if conn:
        criar_tabela(conn)

        df = carregar_dados_csv(r"D:\FIAP\FIAP_FASE3\Arduino.csv")
        inserir_dados_csv(conn, df)

        # Ler dados
        print("Dados na tabela após inserção:")
        ler_dados(conn)

        # Teste de atualização e exclusão
        atualizar_dados(conn, sensor_id=1, new_humidity=60.0)
        excluir_dados(conn, sensor_id=1)

        # Geração do dashboard
        gerar_dashboard(conn)

        conn.close()
        print("Conexão com o banco de dados encerrada.")


if __name__ == "__main__":
    main()
