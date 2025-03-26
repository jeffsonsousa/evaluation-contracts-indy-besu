from bs4 import BeautifulSoup
import os
import pandas as pd
import re

# Nome do script/função analisada (facilita modificações futuras)
script_name = "createCredentialDefinition"

def extract_summary_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    tables = soup.find_all('table')
    summary_data = []
    resource_data = []

    for table in tables:
        # --- SUMÁRIO DE MÉTRICAS ---
        if 'Summary of performance metrics' in str(table):
            rows = table.find_all('tr')[1:]  # skip header
            for row in rows:
                cols = [td.text.strip() for td in row.find_all('td')]
                if len(cols) == 8:
                    try:
                        summary_data.append({
                            'Round': cols[0],
                            'Success': int(cols[1]),
                            'Fail': int(cols[2]),
                            'SendRate': float(cols[3]) if cols[3] != '-' else None,
                            'MaxLatency': float(cols[4]) if cols[4] != '-' else None,
                            'MinLatency': float(cols[5]) if cols[5] != '-' else None,
                            'AvgLatency': float(cols[6]) if cols[6] != '-' else None,
                            'Throughput': float(cols[7]) if cols[7] != '-' else None
                        })
                    except ValueError:
                        print(f"⚠ Erro ao converter dados no arquivo {file_path}: {cols}")

        # --- RECURSOS POR CONTAINER ---
        if table.find('th') and 'CPU%(max)' in table.text:
            print(f"✅ Tabela de recursos detectada no arquivo: {file_path}")  # debug opcional
            rows = table.find_all('tr')[1:]  # apenas 1 header
            for row in rows:
                cols = [td.text.strip().replace('-', '0') for td in row.find_all('td')]
                if len(cols) >= 9:
                    try:
                        resource_data.append({
                            'Node': cols[0],
                            'CPU%(max)': float(cols[1]),
                            'CPU%(avg)': float(cols[2]),
                            'Memory(max) [GB]': float(cols[3]),
                            'Memory(avg) [GB]': float(cols[4]),
                            'Traffic In [B]': float(cols[5]),
                            'Traffic Out [B]': float(cols[6]),
                            'Disc Write [B]': float(cols[7]),
                            'Disc Read [B]': float(cols[8]),
                            'Disc Write [MB]': round(float(cols[7]) / (1024 * 1024), 4),
                            'Disc Read [KB]': round(float(cols[8]) / 1024, 4),
                            'Disc Read [GB]': round(float(cols[8]) / (1024 ** 3), 6)
                        })
                    except ValueError:
                        print(f"⚠ Erro ao converter dados de recurso no arquivo {file_path}: {cols}")
    return summary_data, resource_data


def extract_tps_from_filename(filename):
    match = re.search(r'report_(\d+)', filename)
    if match:
        return int(match.group(1))
    return None


def parse_all_reports(folder_path):
    all_summary = []
    all_resources = []
    for file in os.listdir(folder_path):
        if file.startswith(script_name) and file.endswith(".html"):
            file_path = os.path.join(folder_path, file)
            summary_data, resource_data = extract_summary_from_html(file_path)
            tps = extract_tps_from_filename(file)
            for entry in summary_data:
                entry['ReportFile'] = file
                entry['ConfiguredTPS'] = tps
                all_summary.append(entry)
            for entry in resource_data:
                entry['ReportFile'] = file
                entry['Rate'] = tps
                all_resources.append(entry)
    return pd.DataFrame(all_summary), pd.DataFrame(all_resources)


if __name__ == "__main__":
    report_folder = f"./reports/{script_name}/"
    df_summary, df_resources = parse_all_reports(report_folder)

    output_summary_csv = os.path.join(report_folder, f"{script_name}_summary_metrics.csv")
    output_resources_csv = os.path.join(report_folder, f"{script_name}_resource_metrics.csv")

    df_summary.to_csv(output_summary_csv, index=False)
    df_resources.to_csv(output_resources_csv, index=False)

    print(f"✅ Arquivos salvos com sucesso:")
    print(f"  - {output_summary_csv}")
    print(f"  - {output_resources_csv}")
