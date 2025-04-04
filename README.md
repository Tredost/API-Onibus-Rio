# 🚌 API de Ônibus do Rio - Versão Otimizada

### ⚠️ Por que isso existe?

A API oficial da Prefeitura do Rio de Janeiro ([dados.mobilidade.rio/gps/sppo](https://dados.mobilidade.rio/gps/sppo)) retorna arquivos com **mais de 100MB**, o que **trava fluxos** e dificulta análises simples.

Por isso, desenvolvi essa **API intermediária leve**, ideal para consumo em automações, dashboards e scripts.

### ✅ Funcionalidades

- 🌐 Consulta eficiente via `stream` e descompressão `gzip`.
- 🧹 Filtragem: somente ônibus em movimento (`velocidade > 0`).
- 🕒 Conversão de timestamps para formato legível.
- ⚡ Cálculo de atraso de transmissão (diferença entre servidor e GPS).
- 📦 Resposta com limite de tamanho (500 registros).
- ⚙️ Hospedável gratuitamente via [Railway](https://railway.app/).

## 📡 Endpoints Disponíveis

### `GET /`

- **Descrição:** Verifica se a API está online.
- **Resposta:**
```json
"API de ônibus do RJ online 🚌💨 - by Tredost"
```
### `GET /onibus`

- **Descrição:** Retorna uma lista de ônibus em movimento no Rio de Janeiro, com dados tratados e resposta leve (máximo 500 registros).
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

## 🚀 Como usar localmente

```bash
git clone https://github.com/Tredost/API-Onibus-Rio.git
cd API-Onibus-Rio
pip install -r requirements.txt
python app.py
Acesse em http://localhost:5000/onibus.
```
