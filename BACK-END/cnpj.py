import pandas as pd
import re

def calcular_dv_cnpj_base(cnpj_base):
    """
    Recebe um CNPJ base (12 dígitos) e retorna os dois dígitos verificadores calculados.
    """
    cnpj_base = re.sub(r'\D', '', str(cnpj_base))
    if len(cnpj_base) != 12:
        return 'Base inválida'
    
    # Cálculo do primeiro dígito verificador
    pesos1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    soma1 = sum(int(d) * p for d, p in zip(cnpj_base, pesos1))
    dv1 = 11 - (soma1 % 11)
    dv1 = 0 if dv1 >= 10 else dv1
    
    # Cálculo do segundo dígito verificador
    cnpj_13 = cnpj_base + str(dv1)
    pesos2 = [6,5,4,3,2,9,8,7,6,5,4,3,2]
    soma2 = sum(int(d) * p for d, p in zip(cnpj_13, pesos2))
    dv2 = 11 - (soma2 % 11)
    dv2 = 0 if dv2 >= 10 else dv2
    
    return f"{dv1}{dv2}"

def extrair_base_cnpj(cnpj):
    """
    Extrai os 8 primeiros dígitos do CNPJ e adiciona '0001' ao final.
    """
    cnpj_limpo = re.sub(r'\D', '', str(cnpj))
    base_8 = cnpj_limpo[:8].zfill(8)  # Garante 8 dígitos
    return f"{base_8}0001"

# Carrega o arquivo CSV
df = pd.read_csv('empresas.csv')
df.columns = df.columns.str.strip()  # Remove espaços dos nomes das colunas

# Aplica as funções para criar as novas colunas
df['Base CNPJ'] = df['CNPJ'].apply(extrair_base_cnpj)
df['DV Calculado'] = df['Base CNPJ'].apply(calcular_dv_cnpj_base)
df['CNPJ Completo'] = df['Base CNPJ'] + df['DV Calculado']

# Exibe o resultado no terminal
print("\nResultado do processamento:")
print(df[['Nome da empresa', 'CNPJ', 'Base CNPJ', 'DV Calculado', 'CNPJ Completo']].to_string(index=False))

# Salva em Excel
df.to_excel('cnpjs_bases_com_dv.xlsx', index=False)
print("\nArquivo 'cnpjs_bases_com_dv.xlsx' gerado com sucesso!")
