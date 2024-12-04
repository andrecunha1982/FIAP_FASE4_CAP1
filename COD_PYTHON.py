import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "C:/Users/Amanda/OneDrive/Área de Trabalho/FASE04_CAP1/CAP1_FASE4/Arduino.csv"
try:
    data = pd.read_csv(file_path)
    print("Arquivo carregado com sucesso!")
except FileNotFoundError:
    raise FileNotFoundError(f"O arquivo {file_path} não foi encontrado. Verifique o caminho do arquivo.")

# Pré-processamento dos dados
data = data.drop(columns=['sensor_id'])  
data = data.dropna()  

if data.empty:
    raise ValueError("O dataset está vazio após a remoção de valores ausentes.")

data['Timestamp'] = pd.to_datetime(data['Timestamp'])  

# Seleção de features
features = ['Temperatura', 'Umidade', 'pH', 'Fósforo', 'Potássio']
X = data[features]
y = data['IrrigaçãoOn']

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
    sns.lineplot(x=data['Timestamp'], y=data['Umidade'], label='Umidade', marker='o')
    plt.xlabel('Timestamp')
    plt.ylabel('Umidade')
    plt.title('Variação da Umidade do Solo ao Longo do Tempo')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

if st.sidebar.checkbox("Níveis de Nutrientes ao Longo do Tempo"):
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=data['Timestamp'], y=data['Fósforo'], label='Fósforo', marker='o')
    sns.lineplot(x=data['Timestamp'], y=data['Potássio'], label='Potássio', marker='o')
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
    'Temperatura': st.sidebar.slider("Temperatura (°C)", min_value=10, max_value=50, value=25),
    'Umidade': st.sidebar.slider("Umidade (%)", min_value=0, max_value=100, value=50),
    'pH': st.sidebar.slider("pH", min_value=3.0, max_value=14.0, value=7.0),
    'Fósforo': st.sidebar.slider("Fósforo (mg/L)", min_value=0, max_value=100, value=50),
    'Potássio': st.sidebar.slider("Potássio (mg/L)", min_value=0, max_value=100, value=50)
}

input_df = pd.DataFrame([input_data])
predicted_action = model.predict(input_df)[0]
st.sidebar.write(f"Previsão de Ação: {'Irrigar' if predicted_action == 1 else 'Não Irrigar'}")


st.success("O sistema está pronto para uso! Explore os gráficos e faça previsões com base nos seus parâmetros.")



# Passos para Executar o Streamlit
#Abra o terminal ou prompt de comando.

#Navegue até o diretório onde está o seu script:

#cd "C:/Users/Amanda/OneDrive/Área de Trabalho/FASE04_CAP1/CAP1_FASE4" (de acordo o caminho do arquivo em seu computador)
#Execute o script com o Streamlit:

#streamlit run COD_PYTHON.py
#
