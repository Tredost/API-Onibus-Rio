from flask import Flask, jsonify, Response
import requests
from datetime import datetime
import os
import json
import ijson
import gzip

app = Flask(__name__)

MAX_ITENS = 500  # tem q limitar pq a api da prefeitura manda 120mb e trava o chip de batata da n8n

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
        response = requests.get(url, stream=True)
        response.raw.decode_content = True
        response.raise_for_status()

        tratados = []
        itens = ijson.items(response.raw, 'item')

        for onibus in itens:
            if float(onibus.get("velocidade", 0)) > 0:
                item = tratar_dado(onibus)
                if item:
                    tratados.append(item)
            if len(tratados) >= MAX_ITENS:
                break

        # ordenar e formatar datas
        tratados.sort(key=lambda x: x["datahora"], reverse=True)
        for item in tratados:
            item["datahora"] = item["datahora"].strftime("%Y-%m-%d %H:%M:%S")
            item["datahoraservidor"] = item["datahoraservidor"].strftime("%Y-%m-%d %H:%M:%S")

        return jsonify(tratados)

    except Exception as e:
        return jsonify({"erro": f"Erro ao processar dados: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)