# FarmTech Solutions - Sistema de Irrigação Inteligente (Fase 04)
## Descrição do Projeto
Este projeto, desenvolvido para a empresa FarmTech Solutions, é um sistema de irrigação inteligente que monitora dados ambientais (umidade, intensidade de luz para simular pH, e níveis de nutrientes representados por botões) com sensores físicos conectados ao microcontrolador ESP32. Os dados coletados pelos sensores são armazenados em um banco de dados Oracle, e o sistema permite operações CRUD (Criar, Ler, Atualizar e Deletar) sobre esses dados. O objetivo é otimizar a irrigação agrícola, utilizando uma lógica de decisão que controla automaticamente a bomba d’água representada por um relé.

Este README descreve o funcionamento do projeto, a estrutura do código e as instruções de configuração.

## Objetivos do Projeto
Considerando que na Fase 3 foi desenvolvido um projeto para monitorar a umidade do solo, níveis de nutrientes (P e K), e o pH (simulado com um sensor de intensidade de luz); controlar automaticamente a irrigação, acionando a bomba d'água (relé) conforme os dados coletados; armazenar dados no banco de dados Oracle e realizar operações CRUD através de um script Python; criar visualizações de dados com um dashboard em Python, integração com API pública para previsão meteorológica, e análise estatística com R, essa nova fase será focada nos seguintes desafios:

Incorporar Scikit-learn: utilização da biblioteca Scikit-learn para aprimorar a inteligência do sistema de irrigação automatizado. 

Implementar Streamlit: aprimoração do dashboard do projeto utilizando Streamlit, criando uma interface interativa onde os dados do sistema de irrigação podem ser visualizados em tempo real.

Adicionar display LCD no Wokwi: implementar um display LCD conectado ao ESP32 no Wokwi, barramento I2C (pinos SDA e SCL), para mostrar as principais métricas em tempo real, umidade, níveis de nutrientes e status da irrigação.

Monitoramento com Serial Plotter: implementação do Serial Plotter para monitorar uma ou mais variáveis do projeto.

Otimização de Memória no ESP32: revisão e otimização do uso das variáveis no código C/C++ do ESP32.

## Estrutura do Projeto:

📂 fase04
│
├── 📁 circuito
│   └── sketch.ino         # Código C++ para ESP32
│   └── diagram.json       # Diagrama do projeto para Wokwi
│   └── libraries.txt      # Bibliotecas C++ utilizadas no projeto
│   └── Video Youtube.txt  # Link do video do funcionamento do projeto
│   └── wokwi-project.txt  # Link para emulação do projeto no Wokwi.com
│
├── 📁 dados
│   └── Arduino.csv        # Dados coletados dos sensores no formato CSV
│
├── 📁 scripts
│   └── Codigo_Pyhton_consultaBD.py         # Script Python para integração com o banco de dados Oracle
│
└── README.md                     # Documentação do projeto

## Componentes do Projeto
### 1. Sensores (Simulados no Wokwi)
- Umidade: Sensor DHT22.

- pH: Sensor de intensidade de luz (LDR) simula o sensor de pH.

- Nutrientes P e K: Simulados com botões, representando valores booleanos de presença ou ausência.

- Relé: Representa a bomba de irrigação.

- RTC: Módulo RTC para controle de data e hora de cada registro;
 
### 2. Microcontrolador ESP32
O ESP32 coleta os dados dos sensores e determina quando a bomba d’água deve ser acionada. O código foi implementado em C++ e simulado na plataforma Wokwi.
![image](https://github.com/user-attachments/assets/dc25bdb1-cb25-4d4a-b729-2ee270780969)

O projeto pode ser executado neste [link](https://wokwi.com/projects/416204742855791617)

**Alterações e Justificativas com relação a Fase 03:**

Com o apoio de Inteligencia Artificial Generativa, foi executada uma revisão de código com o objetivo de realizar otimizações quando utilizar tipos de dados inteiros, floats e chars para economizar memória, garantindo que o sistema rode de maneira mais eficiente. Como resultado dessa análise tivemos: 

- **Uso de tipos de dados otimizados:**
    - Substituí float por int16_t ou uint16_t sempre que possível, convertendo os valores apenas para exibição (caso necessário) para economizar memória.
    - Substituí String por char arrays e snprintf para manipular strings, evitando fragmentação de heap.
    
- **Uso de macros e constantes:**
    - Defini constantes para evitar cálculos repetitivos no código.
    - Usei const ao invés de variáveis globais mutáveis, quando aplicável.
    
- **Redução de operações desnecessárias no loop:**
    - Mantenho cálculos mínimos e reutilizo valores calculados anteriormente.
    
- **Otimização do cálculo do pH:**
    - Transformei a escala de pH em uint8_t por ser uma escala discreta e limitada a valores entre 0 e 14.

**Benefícios da otimização**

- **Memória:** A substituição de String por char arrays reduz fragmentação da memória e melhora desempenho.

- **Desempenho:** Tipos como uint8_t e uint16_t economizam memória comparado a int ou float, especialmente em sistemas embarcados.

- **Legibilidade:** O uso de snprintf organiza melhor a formatação e evita overhead do objeto String.

### 3. Banco de Dados Oracle
O banco de dados Oracle armazena os dados dos sensores e os registros de acionamento do relé. A integração é feita através do script Python Codigo_Pyhton_consultaBD.py, que realiza operações CRUD.

############################## EM REVISÃO


### 5. Dashboard 
Para visualização dos dados, foi criado um dashboard com a  biblioteca matplotlib dentro do codigo pyhton:

![Captura de tela 2024-11-13 101959](https://github.com/user-attachments/assets/ba1efe27-fdfb-492a-adcb-ded18bde056d)

## Funcionamento

ESP32:
- O código do ESP32, em sketch.ino, configura os sensores e o relé.
- Ele coleta os dados e aplica a lógica de decisão para acionar ou não a bomba d'água.
- Os dados são exibidos no Monitor Serial para fácil acesso e coleta.

Integração com Banco de Dados Oracle (Script Python):
- O arquivo Codigo_Pyhton_consultaBD.py conecta-se ao banco de dados Oracle.
- Utiliza o arquivo CSV (Arduino.csv) para carregar dados simulados.
- Realiza operações CRUD (Criar, Ler, Atualizar, Deletar) com as informações do solo.
- Pode ser configurado para registrar o status da irrigação conforme os dados dos sensores.

Pré-requisitos:
- Python 3.x instalado.
- Bibliotecas cx_Oracle: Para conectar o Python ao Oracle, instale via pip install cx_Oracle.
- import oracledb
- import pandas as pd
- import matplotlib.pyplot
- Wokwi: Para compilar e enviar o código ao ESP32.
- Conta no Oracle Database (pode ser local ou na nuvem).

### Como Configurar e Rodar o Projeto

1. Configuração do Circuito no Wokwi
Acesse Wokwi e configure o circuito conforme descrito abaixo:
- Copie o Arquivo diagram.json para obter o ESP e os outros componentes.
- Carregue o código sketch.ino no ESP32 para monitorar os sensores.
- Abra o Monitor Serial para visualizar os dados dos sensores.

2. Exportação dos Dados
- Copie os dados do Monitor Serial do Wokwi e cole no arquivo Arduino.csv localizado na pasta dados.
- Ajuste os dados conforme necessário para simular um cenário real.
  
3. Script Python - Codigo_Pyhton_consultaBD.py
- Abra o arquivo Codigo_Pyhton_consultaBD.py e configure a conexão com o banco de dados com os parâmetros corretos.
- Execute o script para importar dados do arquivo CSV e realizar operações CRUD.


## Lógica de Decisão da Irrigação
A bomba de irrigação é acionada com base na Umidade (se a umidade do solo estiver abaixo de um certo limite, a irrigação é ligada).

Níveis de P e K: Se ambos os botões estiverem pressionados, o sistema assume níveis baixos de nutrientes.

pH: O sensor LDR simula o pH e, dependendo da intensidade da luz, determina o nível de acidez do solo.

Cada critério pode ser ajustado para otimizar o uso da água, economizando recursos e maximizando a produtividade.

## Documentação Adicional

O vídeo de demonstração do projeto está disponível aqui: [https://www.youtube.com/watch?v=7aTtdq6nKZQ].

## Tecnologias Utilizadas
- Microcontrolador ESP32
- Python 3.x
- Oracle Database
- Arduino IDE
- Matplotlib
- Wokwi

## Conclusão
Este projeto demonstra como conectar sensores físicos a uma plataforma digital para otimizar a irrigação agrícola, integrando dados de sensores a um banco de dados e criando um sistema de irrigação inteligente. Essa solução é uma contribuição para o avanço da FarmTech Solutions, com foco na eficiência de recursos hídricos e melhoria da produção agrícola.
