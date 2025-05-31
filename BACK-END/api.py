from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import re

app = Flask(__name__)
CORS(app)

def calcular_dv_cnpj_base(cnpj_base):
    cnpj_base = re.sub(r'\D', '', str(cnpj_base))
    if len(cnpj_base) != 12:
        return 'Base inválida'
    
    pesos1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    soma1 = sum(int(d) * p for d, p in zip(cnpj_base, pesos1))
    dv1 = 11 - (soma1 % 11)
    dv1 = 0 if dv1 >= 10 else dv1
    
    cnpj_13 = cnpj_base + str(dv1)
    pesos2 = [6,5,4,3,2,9,8,7,6,5,4,3,2]
    soma2 = sum(int(d) * p for d, p in zip(cnpj_13, pesos2))
    dv2 = 11 - (soma2 % 11)
    dv2 = 0 if dv2 >= 10 else dv2
    
    return f"{dv1}{dv2}"

def extrair_base_cnpj(cnpj):
    cnpj_limpo = re.sub(r'\D', '', str(cnpj))
    base_8 = cnpj_limpo[:8].zfill(8)
    return f"{base_8}0001"

# Carrega o CSV e prepara os dados
df = pd.read_csv('empresas.csv', sep=',') 
df.columns = df.columns.str.strip()
df['Base CNPJ'] = df['CNPJ'].apply(extrair_base_cnpj)
df['DV Calculado'] = df['Base CNPJ'].apply(calcular_dv_cnpj_base)
df['CNPJ Completo'] = df['Base CNPJ'] + df['DV Calculado']

@app.route('/buscar')
def buscar():
    termo = request.args.get('q', '').strip().lower()
    

    if termo.isdigit():
        n = int(termo)
        resultados = df.head(n)
        resposta = resultados[['Nome da empresa', 'CNPJ']].to_dict(orient='records')
        return jsonify(resposta)
    
    resultados = df[df['Nome da empresa'].str.lower().str.contains(termo, na=False, regex=False)]
    resultados = resultados.sort_values(by='Nome da empresa', key=lambda x: x.str.len())
    resposta = resultados[['Nome da empresa', 'CNPJ']].to_dict(orient='records')
    return jsonify(resposta)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
