"""Análise exploratória dos preços de combustíveis da ANP em 2024.

Os arquivos semestrais são lidos diretamente dos ZIPs guardados em dados/.
"""
from pathlib import Path
from zipfile import ZipFile
from io import TextIOWrapper

import pandas as pd
import matplotlib.pyplot as plt

PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_DADOS = PASTA_PROJETO / "dados"
PASTA_RESULTADOS = PASTA_PROJETO / "relatorio"
PASTA_GRAFICOS = PASTA_PROJETO / "graficos"
PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

ARQUIVOS_ZIP = [
    PASTA_DADOS / "ca-2024-01.zip",
    PASTA_DADOS / "ca-2024-02.zip",
]
COMBUSTIVEIS = ["GASOLINA", "ETANOL", "DIESEL S10"]


def ler_csv_anp(caminho_zip):
    """Lê o CSV semestral armazenado dentro do ZIP da ANP."""
    if not caminho_zip.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_zip}")
    with ZipFile(caminho_zip) as arquivo_zip:
        arquivos_csv = [
            nome for nome in arquivo_zip.namelist()
            if nome.lower().endswith(".csv")
        ]
        if not arquivos_csv:
            raise FileNotFoundError(f"Nenhum CSV encontrado em {caminho_zip.name}")
        with arquivo_zip.open(arquivos_csv[0]) as arquivo_csv:
            return pd.read_csv(
                TextIOWrapper(arquivo_csv, encoding="latin1"),
                sep=";",
                dtype=str,
                low_memory=False,
            )


def converter_preco(coluna):
    """Converte preço no padrão brasileiro para número decimal."""
    texto = (
        coluna.astype("string")
        .str.replace("R$", "", regex=False)
        .str.replace(" ", "", regex=False)
    )
    tem_virgula = texto.str.contains(",", na=False)
    texto.loc[tem_virgula] = (
        texto.loc[tem_virgula]
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    return pd.to_numeric(texto, errors="coerce")


def main():
    bases = [ler_csv_anp(caminho) for caminho in ARQUIVOS_ZIP]
    dados = pd.concat(bases, ignore_index=True)
    dados.columns = (
        dados.columns.str.replace("ï»¿", "", regex=False)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )

    for coluna in ["Produto", "Municipio", "Estado - Sigla", "Regiao - Sigla"]:
        dados[coluna] = dados[coluna].astype("string").str.strip()
    dados["Produto"] = dados["Produto"].str.upper()
    dados["Preco"] = converter_preco(dados["Valor de Venda"])
    dados["Data da Coleta"] = pd.to_datetime(
        dados["Data da Coleta"], format="%d/%m/%Y", errors="coerce"
    )

    etapas = [{"Etapa": "Base original", "Registros": len(dados)}]
    dados = dados[dados["Produto"].isin(COMBUSTIVEIS)].copy()
    etapas.append({"Etapa": "Após filtro dos combustíveis", "Registros": len(dados)})
    dados = dados.dropna(subset=["Preco", "Data da Coleta"])
    etapas.append({"Etapa": "Após remover preço/data inválidos", "Registros": len(dados)})
    dados = dados[dados["Preco"] > 0].copy()
    etapas.append({"Etapa": "Após manter preços positivos", "Registros": len(dados)})
    dados = dados[dados["Data da Coleta"].dt.year == 2024].copy()
    etapas.append({"Etapa": "Após filtro de 2024", "Registros": len(dados)})

    if dados.empty:
        raise ValueError("Nenhum registro válido foi encontrado após os filtros.")

    dados["Mes"] = dados["Data da Coleta"].dt.month
    dados["Semana"] = dados["Data da Coleta"].dt.to_period("W").dt.start_time

    print(pd.DataFrame(etapas).to_string(index=False))
    print(
        f"Período: {dados['Data da Coleta'].min():%d/%m/%Y} "
        f"a {dados['Data da Coleta'].max():%d/%m/%Y}"
    )
    print("\nRegistros por combustível:")
    print(dados["Produto"].value_counts())

    # Estatísticas descritivas.
    estatisticas = dados.groupby("Produto")["Preco"].agg(
        Registros="count",
        Media="mean",
        Mediana="median",
        Minimo="min",
        Maximo="max",
        Desvio_Padrao="std",
    ).round(2)
    estatisticas.to_csv(
        PASTA_RESULTADOS / "estatisticas_combustiveis.csv",
        encoding="utf-8-sig",
    )

    # Diagnóstico de possíveis extremos pelo critério 1,5 x IQR.
    def resumir_extremos(grupo):
        q1, q3 = grupo["Preco"].quantile([0.25, 0.75])
        iqr = q3 - q1
        fora = (grupo["Preco"] < q1 - 1.5 * iqr) | (grupo["Preco"] > q3 + 1.5 * iqr)
        return pd.Series({"Q1": q1, "Q3": q3, "Possiveis_extremos": int(fora.sum())})

    extremos = dados.groupby("Produto").apply(
        resumir_extremos, include_groups=False
    ).round(2)
    extremos.to_csv(PASTA_RESULTADOS / "diagnostico_extremos_iqr.csv", encoding="utf-8-sig")

    dados.to_csv(
        PASTA_RESULTADOS / "dados_tratados.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Médias por região.
    media_regiao = dados.groupby(
        ["Regiao - Sigla", "Produto"], as_index=False
    ).agg(Preco_medio=("Preco", "mean"), Registros=("Preco", "size"))
    media_regiao["Preco_medio"] = media_regiao["Preco_medio"].round(2)
    media_regiao.to_csv(
        PASTA_RESULTADOS / "preco_medio_regiao.csv",
        index=False,
        encoding="utf-8-sig",
    )

    grafico_regiao = media_regiao.pivot(
        index="Regiao - Sigla", columns="Produto", values="Preco_medio"
    )
    grafico_regiao.plot(kind="bar", figsize=(10, 6))
    plt.title("Preço médio registrado por região e combustível — 2024")
    plt.xlabel("Região")
    plt.ylabel("Preço médio (R$/litro)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(PASTA_GRAFICOS / "preco_medio_regiao.png", dpi=160)
    plt.close()

    # Médias mensais.
    media_mensal = dados.groupby(
        ["Mes", "Produto"], as_index=False
    )["Preco"].mean()
    media_mensal["Preco"] = media_mensal["Preco"].round(2)
    media_mensal.to_csv(
        PASTA_RESULTADOS / "preco_medio_mensal.csv",
        index=False,
        encoding="utf-8-sig",
    )

    media_mensal.pivot(index="Mes", columns="Produto", values="Preco").plot(
        kind="line", marker="o", figsize=(11, 6)
    )
    plt.title("Preço médio registrado por mês — Brasil, 2024")
    plt.xlabel("Mês")
    plt.ylabel("Preço médio (R$/litro)")
    plt.xticks(range(1, 13))
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PASTA_GRAFICOS / "evolucao_mensal.png", dpi=160)
    plt.close()

    # Médias semanais para acompanhar oscilações dentro de cada mês.
    media_semanal = dados.groupby(
        ["Semana", "Produto"], as_index=False
    )["Preco"].mean()
    media_semanal.to_csv(
        PASTA_RESULTADOS / "preco_medio_semanal.csv",
        index=False,
        encoding="utf-8-sig",
    )
    media_semanal.pivot(index="Semana", columns="Produto", values="Preco").plot(
        kind="line", figsize=(12, 6)
    )
    plt.title("Preço médio registrado por semana — Brasil, 2024")
    plt.xlabel("Semana")
    plt.ylabel("Preço médio (R$/litro)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PASTA_GRAFICOS / "evolucao_semanal.png", dpi=160)
    plt.close()

    print(f"\nTabelas salvas em: {PASTA_RESULTADOS}")
    print(f"Gráficos salvos em: {PASTA_GRAFICOS}")


if __name__ == "__main__":
    main()
