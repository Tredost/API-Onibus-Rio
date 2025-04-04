from flask import Flask, jsonify, Response
import requests
from datetime import datetime
import os
import json

app = Flask(__name__)

MAX_REGISTROS = 20 # tem q limitar pq a api da prefeitura manda 120mb e trava o chip de batata da n8n

def tratar_dado(dado):
    try:
        return {
            "ordem": dado["ordem"],
            "linha": dado["linha"],
            "latitude": float(dado["latitude"].replace(",", ".")),
            "longitude": float(dado["longitude"].replace(",", ".")),
            "datahora": datetime.fromtimestamp(int(dado["datahora"]) / 1000),
            "datahoraservidor": datetime.fromtimestamp(int(dado["datahoraservidor"]) / 1000),
            "atraso_ms": int(dado["datahoraservidor"]) - int(dado["datahora"]),
            "velocidade": float(dado["velocidade"])
        }
    except Exception as e:
        print(f"Erro ao tratar dado: {e}")
        return None

@app.route("/", methods=["GET"])
def index():
    return "API de ônibus do RJ online 🚌💨 - by Tredost"

@app.route("/onibus", methods=["GET"])
def dados_onibus():
    url = "https://dados.mobilidade.rio/gps/sppo"

    try:
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()

        tratados = []
        for onibus in dados[:MAX_REGISTROS]:
            if float(onibus["velocidade"]) > 0:
                item = tratar_dado(onibus)
                if item:
                    tratados.append(item)


        # Ordenar do mais recente para o mais antigo
        tratados.sort(key=lambda x: x["datahora"], reverse=True)

        # Remover o campo datetime (pra serializar corretamente depois)
        for item in tratados:
            item["datahora"] = item["datahora"].strftime("%Y-%m-%d %H:%M:%S")
            item["datahoraservidor"] = item["datahoraservidor"].strftime("%Y-%m-%d %H:%M:%S")

        # Limitar a 10 MB de resposta
        tamanho_total = 0
        resposta_final = []
        for item in tratados:
            json_bytes = json.dumps(item).encode("utf-8")
            if tamanho_total + len(json_bytes) > MAX_RESPONSE_SIZE_BYTES:
                break
            resposta_final.append(item)
            tamanho_total += len(json_bytes)

        return Response(json.dumps(resposta_final), mimetype='application/json')

    except requests.exceptions.RequestException as e:
        return jsonify({"erro": f"Erro na requisição à API da prefeitura: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

