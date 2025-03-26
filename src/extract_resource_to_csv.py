import pandas as pd
import os

# Nome do script/função analisada (facilita modificações futuras)
script_name = 'createCredentialDefinition'

# Caminho para o arquivo CSV original
input_csv_path = f'./reports/{script_name}/{script_name}_resource_metrics.csv'

# Leitura do CSV
df = pd.read_csv(input_csv_path)

# Converter a coluna Rate para numérica (pode conter strings ou valores ausentes)
df['Rate'] = pd.to_numeric(df['Rate'], errors='coerce')

# Criar diretório de saída
output_dir = f'{script_name}_resource_metrics_by_tps'
os.makedirs(output_dir, exist_ok=True)

# Identificar os valores únicos de TPS (Rate)
unique_tps = df['Rate'].dropna().unique()

# Salvar um CSV separado por TPS
for tps in unique_tps:
    df_tps = df[df['Rate'] == tps]
    df_tps.to_csv(f'{output_dir}/{script_name}_resource_metrics_tps_{int(tps)}.csv', index=False)

print(f'✅ CSVs separados por TPS salvos em: {output_dir}')
