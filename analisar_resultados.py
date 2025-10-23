import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ==============================
# CONFIGURAÇÕES
# ==============================
sns.set(style="whitegrid", palette="muted", font_scale=1.15)
BASE_DIR = Path("results")

# ==============================
# LEITURA DE DADOS
# ==============================
dfs = []

for exec_dir in BASE_DIR.glob("execucao*"):
    exec_name = exec_dir.name
    for csv_file in exec_dir.glob("res*_stats.csv"):
        scen_name = csv_file.stem
        scen_label = scen_name.split("_")[0]
        df = pd.read_csv(csv_file)
        df["Execucao"] = exec_name
        df["Cenario"] = scen_label
        dfs.append(df)

data = pd.concat(dfs, ignore_index=True)

# Renomear cenários
cenario_map = {"res1": "Leve", "res2": "Moderado", "res3": "Pico"}
data["Cenario"] = data["Cenario"].map(cenario_map)

# Converter colunas numéricas (caso sejam strings)
data = data.apply(pd.to_numeric, errors="ignore")

# ==============================
# CÁLCULOS DE MÉTRICAS
# ==============================
# Agrupar por cenário
grouped = data.groupby("Cenario").agg({
    "Request Count": "sum",
    "Failure Count": "sum",
    "Average Response Time": ["mean", "std"],
    "Requests/s": ["mean", "std"],
    "Failures/s": ["mean", "std"]
})

# Calcular taxa de falhas (%)
failure_rate = (data.groupby("Cenario")["Failure Count"].sum() /
                data.groupby("Cenario")["Request Count"].sum()) * 100

grouped.columns = ['_'.join(col).strip() for col in grouped.columns.values]
grouped["Failure Rate (%)"] = failure_rate

# Exportar resumo em CSV
grouped.round(3).to_csv("resumo_metricas.csv")
print("\n===== RESUMO DAS MÉTRICAS POR CENÁRIO =====\n")
print(grouped.round(3))
print("\n(Também salvo como 'resumo_metricas.csv')\n")

# ==============================
# GRÁFICOS ORIGINAIS
# ==============================

# ---------- 1. Proporção de sucesso e falha ----------
data_fail = data.groupby("Cenario")[["Request Count", "Failure Count"]].sum().reset_index()
data_fail["Success Count"] = data_fail["Request Count"] - data_fail["Failure Count"]

plt.figure(figsize=(8,6))
plt.bar(data_fail["Cenario"], data_fail["Success Count"], label="Sucesso", color="#4CAF50")
plt.bar(data_fail["Cenario"], data_fail["Failure Count"],
        bottom=data_fail["Success Count"], label="Falhas", color="#E57373")
plt.title("Proporção de requisições com sucesso e falhas por cenário")
plt.ylabel("Número total de requisições")
plt.xlabel("Cenário")
plt.legend()
plt.tight_layout()
plt.savefig("grafico_sucesso_falhas.png", dpi=300)
plt.show()

# ---------- 2. Taxa de falhas (%) ----------
plt.figure(figsize=(8,6))
sns.barplot(x=failure_rate.index, y=failure_rate.values, color="#E57373")
plt.title("Taxa de falhas (%) por cenário")
plt.ylabel("Falhas (%)")
plt.xlabel("Cenário")
for i, v in enumerate(failure_rate.values):
    plt.text(i, v + 0.05, f"{v:.2f}%", ha="center", va="bottom", fontsize=10)
plt.tight_layout()
plt.savefig("grafico_taxa_falhas.png", dpi=300)
plt.show()

# ==============================
# NOVOS GRÁFICOS E TABELAS
# ==============================

# ---------- 3. Tempo de Resposta (Min, Média, Max) ----------
response_times = data.groupby("Cenario").agg({
    "Min Response Time": "mean",
    "Average Response Time": "mean",
    "Max Response Time": "mean"
}).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(response_times))
width = 0.25

ax.bar([i - width for i in x], response_times["Min Response Time"], 
       width, label="Min", color="#81C784")
ax.bar(x, response_times["Average Response Time"], 
       width, label="Média", color="#FFB74D")
ax.bar([i + width for i in x], response_times["Max Response Time"], 
       width, label="Max", color="#E57373")

ax.set_xlabel("Cenário")
ax.set_ylabel("Tempo de Resposta (ms)")
ax.set_title("Comparação de Tempos de Resposta por Cenário")
ax.set_xticks(x)
ax.set_xticklabels(response_times["Cenario"])
ax.legend()
plt.tight_layout()
plt.savefig("grafico_tempos_resposta.png", dpi=300)
plt.show()

# ---------- 4. Throughput (Requisições/s) ----------
throughput = data.groupby("Cenario")["Requests/s"].agg(["mean", "std"]).reset_index()

plt.figure(figsize=(8, 6))
plt.bar(throughput["Cenario"], throughput["mean"], 
        yerr=throughput["std"], capsize=5, color="#64B5F6")
plt.title("Throughput Médio por Cenário")
plt.ylabel("Requisições/segundo")
plt.xlabel("Cenário")
for i, (mean, std) in enumerate(zip(throughput["mean"], throughput["std"])):
    plt.text(i, mean + std + 0.5, f"{mean:.2f}", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig("grafico_throughput.png", dpi=300)
plt.show()

# ---------- 4. Throughput (Requisições/s) - Gráfico 2 ----------
plt.figure(figsize=(8,6))
sns.barplot(x=grouped.index, y=grouped["Requests/s_mean"], color="#81C784")
plt.title("Throughput Médio por Cenário")
plt.ylabel("Requisições por segundo")
plt.xlabel("Cenário")
plt.tight_layout()
plt.savefig("grafico_throughput2.png", dpi=300)
plt.show()

# ---------- 5. Percentis de Latência ----------
percentiles = data.groupby("Cenario")[["50%", "90%", "95%", "99%"]].mean().reset_index()

plt.figure(figsize=(10, 6))
x = range(len(percentiles))
width = 0.2

plt.bar([i - 1.5*width for i in x], percentiles["50%"], width, label="P50", color="#81C784")
plt.bar([i - 0.5*width for i in x], percentiles["90%"], width, label="P90", color="#FFB74D")
plt.bar([i + 0.5*width for i in x], percentiles["95%"], width, label="P95", color="#FF8A65")
plt.bar([i + 1.5*width for i in x], percentiles["99%"], width, label="P99", color="#E57373")

plt.xlabel("Cenário")
plt.ylabel("Latência (ms)")
plt.title("Percentis de Latência por Cenário")
plt.xticks(x, percentiles["Cenario"])
plt.legend()
plt.tight_layout()
plt.savefig("grafico_percentis_latencia.png", dpi=300)
plt.show()

# ---------- 7. Tabela de Comparação de Percentis ----------
percentiles_table = data.groupby("Cenario")[["50%", "66%", "75%", "90%", "95%", "99%"]].mean()
percentiles_table = percentiles_table.round(2)
percentiles_table.to_csv("tabela_percentis.csv")
print("\n===== TABELA DE PERCENTIS (ms) =====\n")
print(percentiles_table)
print("\n(Salvo como 'tabela_percentis.csv')\n")

# ---------- 8. Tabela de Estabilidade (Desvio Padrão) ----------
stability = data.groupby("Cenario").agg({
    "Average Response Time": ["mean", "std"],
    "Requests/s": ["mean", "std"],
    "Failures/s": ["mean", "std"]
})
stability.columns = ['_'.join(col).strip() for col in stability.columns.values]
stability = stability.round(3)
stability.to_csv("tabela_estabilidade.csv")
print("\n===== TABELA DE ESTABILIDADE (Média ± Desvio Padrão) =====\n")
print(stability)
print("\n(Salvo como 'tabela_estabilidade.csv')\n")

# ---------- 10. Resumo Executivo ----------
summary = pd.DataFrame({
    "Cenário": ["Leve", "Moderado", "Pico"],
    "Total Requisições": data.groupby("Cenario")["Request Count"].sum().values,
    "Taxa de Falhas (%)": failure_rate.values,
    "Tempo Médio (ms)": data.groupby("Cenario")["Average Response Time"].mean().values,
    "P95 (ms)": data.groupby("Cenario")["95%"].mean().values,
    "P99 (ms)": data.groupby("Cenario")["99%"].mean().values,
    "Throughput (req/s)": data.groupby("Cenario")["Requests/s"].mean().values
})
summary = summary.round(2)
summary.to_csv("resumo_executivo.csv", index=False)
print("\n===== RESUMO EXECUTIVO =====\n")
print(summary.to_string(index=False))
print("\n(Salvo como 'resumo_executivo.csv')\n")

print("\n✅ Análise completa! Todos os gráficos e tabelas foram gerados.")
print("\nArquivos gerados:")
print("  - 10 gráficos em PNG (alta resolução)")
print("  - 5 tabelas em CSV")