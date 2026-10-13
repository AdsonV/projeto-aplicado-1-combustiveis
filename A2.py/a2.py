
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# Pastas do projeto
PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_DADOS = PASTA_PROJETO / "dados" / "bruto"
PASTA_RESULTADOS = PASTA_PROJETO / "relatorio"
PASTA_GRAFICOS = PASTA_PROJETO / "graficos"

PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)


# Arquivos da ANP
arquivos = [
    PASTA_DADOS / "Preços semestrais - AUTOMOTIVOS_2024.01.csv",
    PASTA_DADOS / "Preços semestrais - AUTOMOTIVOS_2024.02.csv"
]

lista_dados = []

for arquivo in arquivos:
    if not arquivo.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {arquivo}"
        )

    dados_semestre = pd.read_csv(
        arquivo,
        sep=";",
        encoding="latin1",
        dtype=str,
        low_memory=False
    )

    lista_dados.append(dados_semestre)
    print(f"Arquivo carregado: {arquivo.name}")


# Junta os dois semestres
dados = pd.concat(lista_dados, ignore_index=True)

print("\nDimensões da base original:")
print(f"Linhas: {dados.shape[0]}")
print(f"Colunas: {dados.shape[1]}")


# Limpeza básica
dados = pd.read_csv(
    arquivo,
    sep=";",
    encoding="latin1",
    dtype=str
)

dados["Produto"] = dados["Produto"].str.strip().str.upper()
dados["Municipio"] = dados["Municipio"].str.strip()
dados["Estado - Sigla"] = dados["Estado - Sigla"].str.strip()
dados["Regiao - Sigla"] = dados["Regiao - Sigla"].str.strip()

dados["Valor de Venda"] = pd.to_numeric(
    dados["Valor de Venda"]
    .str.replace("R$", "", regex=False)
    .str.replace(" ", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False),
    errors="coerce"
)

dados["Data da Coleta"] = pd.to_datetime(
    dados["Data da Coleta"],
    format="%d/%m/%Y",
    errors="coerce"
)


# Seleciona os combustíveis do projeto
combustiveis = [
    "GASOLINA",
    "ETANOL",
    "DIESEL S10"
]

dados = dados[
    dados["Produto"].isin(combustiveis)
].copy()

# Remove valores inválidos
dados = dados.dropna(
    subset=["Valor de Venda", "Data da Coleta"]
)

dados = dados[dados["Valor de Venda"] > 0].copy()

# Confere se as datas são de 2024
dados = dados[
    dados["Data da Coleta"].dt.year == 2024
].copy()

if dados.empty:
    raise ValueError(
        "Nenhum registro válido foi encontrado. "
        "Confira os nomes dos produtos e os arquivos."
    )

# Padroniza o nome da coluna de preço
dados = dados.rename(
    columns={"Valor de Venda": "Preco"}
)

# Cria campos para análise temporal
dados["Mes"] = dados["Data da Coleta"].dt.month
dados["Semana"] = (
    dados["Data da Coleta"]
    .dt.to_period("W")
    .dt.start_time
)

# Salva os dados tratados
dados.to_csv(
    PASTA_RESULTADOS / "dados_tratados.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nRegistros após o tratamento:")
print(len(dados))

print("\nQuantidade de registros por combustível:")
print(dados["Produto"].value_counts())


# 1. Estatísticas descritivas
estatisticas = dados.groupby("Produto")["Preco"].agg(
    Quantidade="count",
    Media="mean",
    Mediana="median",
    Minimo="min",
    Maximo="max",
    Desvio_Padrao="std"
).round(2)

print("\nEstatísticas dos preços:")
print(estatisticas)

estatisticas.to_csv(
    PASTA_RESULTADOS / "estatisticas_combustiveis.csv",
    encoding="utf-8-sig"
)


# 2. Preço médio por região
media_regiao = dados.groupby(
    ["Regiao - Sigla", "Produto"]
)["Preco"].mean().round(2).reset_index()

media_regiao.to_csv(
    PASTA_RESULTADOS / "preco_medio_regiao.csv",
    index=False,
    encoding="utf-8-sig"
)

grafico_regiao = media_regiao.pivot(
    index="Regiao - Sigla",
    columns="Produto",
    values="Preco"
)

grafico_regiao.plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("Preço médio por região e combustível - 2024")
plt.xlabel("Região")
plt.ylabel("Preço médio (R$/litro)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(
    PASTA_GRAFICOS / "preco_medio_regiao.png",
    dpi=150
)
plt.close()


# 3. Evolução mensal dos preços
media_mensal = dados.groupby(
    ["Mes", "Produto"]
)["Preco"].mean().round(2).reset_index()

media_mensal.to_csv(
    PASTA_RESULTADOS / "preco_medio_mensal.csv",
    index=False,
    encoding="utf-8-sig"
)

grafico_mensal = media_mensal.pivot(
    index="Mes",
    columns="Produto",
    values="Preco"
)

grafico_mensal.plot(
    kind="line",
    marker="o",
    figsize=(11, 6)
)

plt.title("Evolução mensal dos preços dos combustíveis - 2024")
plt.xlabel("Mês")
plt.ylabel("Preço médio (R$/litro)")
plt.xticks(range(1, 13))
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    PASTA_GRAFICOS / "evolucao_mensal.png",
    dpi=150
)
plt.close()


# 4. Preço médio por estado
media_estado = dados.groupby(
    ["Estado - Sigla", "Produto"]
)["Preco"].agg(
    Preco_Medio="mean",
    Quantidade="count"
).reset_index()

media_estado["Preco_Medio"] = (
    media_estado["Preco_Medio"].round(2)
)

media_estado.to_csv(
    PASTA_RESULTADOS / "preco_medio_estado.csv",
    index=False,
    encoding="utf-8-sig"
)


# 5. Preço médio por município
media_municipio = dados.groupby(
    ["Estado - Sigla", "Municipio", "Produto"]
)["Preco"].agg(
    Preco_Medio="mean",
    Quantidade="count"
).reset_index()

# Mantém municípios com pelo menos cinco registros
media_municipio = media_municipio[
    media_municipio["Quantidade"] >= 5
].copy()

media_municipio["Preco_Medio"] = (
    media_municipio["Preco_Medio"].round(2)
)

media_municipio.to_csv(
    PASTA_RESULTADOS / "preco_medio_municipio.csv",
    index=False,
    encoding="utf-8-sig"
)


# 6. Evolução semanal dos preços
media_semanal = dados.groupby(
    ["Semana", "Produto"]
)["Preco"].mean().reset_index()

media_semanal.to_csv(
    PASTA_RESULTADOS / "preco_medio_semanal.csv",
    index=False,
    encoding="utf-8-sig"
)

grafico_semanal = media_semanal.pivot(
    index="Semana",
    columns="Produto",
    values="Preco"
)

grafico_semanal.plot(
    kind="line",
    figsize=(12, 6)
)

plt.title("Evolução semanal dos preços dos combustíveis - 2024")
plt.xlabel("Semana")
plt.ylabel("Preço médio (R$/litro)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    PASTA_GRAFICOS / "evolucao_semanal.png",
    dpi=150
)
plt.close()


print("\nAnálise concluída!")
print("Tabelas salvas na pasta relatorio.")
print("Gráficos salvos na pasta graficos.")
