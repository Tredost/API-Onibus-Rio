# 🚌 API de Ônibus do Rio - Versão Otimizada

### ⚠️ Por que isso existe?

A API oficial da Prefeitura do Rio de Janeiro ([dados.mobilidade.rio/gps/sppo](https://dados.mobilidade.rio/gps/sppo)) retorna arquivos com **mais de 100MB**, o que **trava fluxos** e dificulta análises simples.

Por isso, desenvolvemos essa **API intermediária leve**, ideal para consumo em automações, dashboards e scripts.

### ✅ Funcionalidades

- 🌐 Consulta eficiente via `stream` e descompressão `gzip`.
- 🧹 Filtragem: somente ônibus em movimento (`velocidade > 0`).
- 🕒 Conversão de timestamps para formato legível.
- ⚡ Cálculo de atraso de transmissão (diferença entre servidor e GPS).
- 📦 Resposta com limite de tamanho (500 registros).
- ⚙️ Hospedável gratuitamente via [Railway](https://railway.app/).

## 📡 Endpoints Disponíveis

### `GET /`

- **Verifica se a API está online.** 
- **Resposta:**
```json
"API de ônibus otimizada do RJ online 🚌💨 - by Tredost"
```
### `GET /onibus_tratados`

- **Retorna uma lista de ônibus em movimento no Rio de Janeiro, com dados tratados e resposta leve.**
  
- 📌 Filtra apenas ônibus com velocidade > 0.

- 🧹 Padroniza as coordenadas GPS.

- ⏱️ Converte timestamps para o formato YYYY-MM-DD HH:mm:ss.

- ⌛ Calcula o atraso de transmissão (atraso_ms).

- 📉 Ordena os registros do mais recente para o mais antigo.

- 📦 Limita a resposta a 500 registros para não travar sistemas externos (como o N8N).
- **Resposta:**
```json
[
  {
    "ordem": "B32772",
    "linha": "910",
    "latitude": -22.85173,
    "longitude": -43.32666,
    "datahora": "2025-04-04 19:35:00",
    "datahoraservidor": "2025-04-04 19:35:24",
    "atraso_ms": 24000,
    "velocidade": 23.4
  },
  {
    "ordem": "A12345",
    "linha": "473",
    "latitude": -22.91111,
    "longitude": -43.18555,
    "datahora": "2025-04-04 19:34:50",
    "datahoraservidor": "2025-04-04 19:35:10",
    "atraso_ms": 20000,
    "velocidade": 17.8
  }
]
```
### `GET /onibus_bruto`

- **Retorna uma lista de ônibus em movimento no Rio de Janeiro, com dados brutos mas com resposta leve.**
  
- 📦 Limita a resposta a 500 registros para não travar sistemas externos (como o N8N).
- **Resposta:**
```json
[
  {
    "datahora": "1743815362000",
    "datahoraenvio": "1743815363000",
    "datahoraservidor": "1743815372000",
    "latitude": "-22,92768",
    "linha": "2383",
    "longitude": "-43,57245",
    "ordem": "D12132",
    "velocidade": "0"
  },
  {
    "datahora": "1743815362000",
    "datahoraenvio": "1743815363000",
    "datahoraservidor": "1743815372000",
    "latitude": "-22,89687",
    "linha": "2335",
    "longitude": "-43,56097",
    "ordem": "D12173",
    "velocidade": "0"
  }
]
```

## 🚀 Como usar localmente

```bash
git clone https://github.com/Tredost/API-Onibus-Rio.git
cd API-Onibus-Rio
pip install -r requirements.txt
python app.py
Acesse em http://localhost:5000/
```
