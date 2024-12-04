import oracledb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

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
        data = ler_dados(conn)
        if data is not None:
            print("Dados carregados com sucesso no DataFrame!")
            print(data)  # Exibe o DataFrame
        conn.close()
        print("Conexão com o banco de dados encerrada.")
    # Pré-processamento dos dados
    data = data.drop(columns=['SENSOR_ID'])
    data = data.dropna()  
    if data.empty:
        raise ValueError("O dataset está vazio após a remoção de valores ausentes.")
    
    data['TIMESTAMP'] = pd.to_datetime(data['TIMESTAMP'])  
    # Seleção de features
    features = ['TEMPERATURE', 'HUMIDITY', 'PH', 'PHOSPHORUS', 'POTASSIUM']
    X = data[features]
    y = data['IRRIGATION_ON']
    if X.empty or y.empty:
        raise ValueError("Não há dados suficientes para dividir em treino e teste.")
    # Treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Random Forest Classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    # Avaliar o modelo
    accuracy = model.score(X_test, y_test)
    report = classification_report(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    print(f"Acurácia do Modelo: {accuracy * 100:.2f}%\n")
    print("Relatório de Classificação:")
    print(report)
    print("Matriz de Confusão:")
    print(conf_matrix)

    # Streamlit
    st.title("Sistema de Irrigação Automatizado")
    st.sidebar.header("Opções do Sistema")
    st.sidebar.write("Use as opções abaixo para interagir com o sistema.")
    st.subheader("Dados do Sistema de Irrigação")
    if st.sidebar.checkbox("Exibir Dados Brutos"):
        st.write(data)

    st.subheader("Análise Gráfica")
    if st.sidebar.checkbox("Variação da Umidade ao Longo do Tempo"):
        plt.figure(figsize=(12, 6))
        sns.lineplot(x=data['TIMESTAMP'], y=data['HUMIDITY'], label='Umidade', marker='o')
        plt.xlabel('Timestamp')
        plt.ylabel('Umidade')
        plt.title('Variação da Umidade do Solo ao Longo do Tempo')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

    if st.sidebar.checkbox("Níveis de Nutrientes ao Longo do Tempo"):
        plt.figure(figsize=(12, 6))
        sns.lineplot(x=data['TIMESTAMP'], y=data['PHOSPHORUS'], label='Fósforo', marker='o')
        sns.lineplot(x=data['TIMESTAMP'], y=data['POTASSIUM'], label='Potássio', marker='o')
        plt.xlabel('Timestamp')
        plt.ylabel('Níveis de Nutrientes')
        plt.title('Níveis de Nutrientes ao Longo do Tempo')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)


    st.subheader("Insights Gerados pelo Modelo de Machine Learning")
    st.write(f"Acurácia do Modelo: {accuracy * 100:.2f}%")
    st.text("Relatório de Classificação:")
    st.text(report)
    st.text("Matriz de Confusão:")
    st.write(conf_matrix)


    st.sidebar.header("Previsão de Irrigação")
    input_data = {
        'TEMPERATURE': st.sidebar.slider("Temperatura (°C)", min_value=10, max_value=50, value=25),
        'HUMIDITY': st.sidebar.slider("Umidade (%)", min_value=0, max_value=100, value=50),
        'PH': st.sidebar.slider("pH", min_value=3.0, max_value=14.0, value=7.0),
        'PHOSPHORUS': st.sidebar.slider("Fósforo (mg/L)", min_value=0, max_value=100, value=50),
        'POTASSIUM': st.sidebar.slider("Potássio (mg/L)", min_value=0, max_value=100, value=50)
    }

    input_df = pd.DataFrame([input_data])
    predicted_action = model.predict(input_df)[0]
    st.sidebar.write(f"Previsão de Ação: {'Irrigar' if predicted_action == 1 else 'Não Irrigar'}")


    st.success("O sistema está pronto para uso! Explore os gráficos e faça previsões com base nos seus parâmetros.")

    

if __name__ == "__main__":
    main()
