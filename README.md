# Projeto Aplicado I — Preços de Combustíveis no Brasil

Projeto individual da disciplina **Projeto Aplicado I**, do curso de Ciência de Dados.

## Tema e recorte

Análise exploratória dos preços de revenda no Brasil em **2024**, com foco em gasolina comum, etanol hidratado e diesel S10. O projeto investiga variações ao longo do ano e diferenças entre regiões, estados e municípios.

## Fonte dos dados

Os dados são da Agência Nacional do Petróleo, Gás Natural e Biocombustíveis (ANP), série histórica de preços de combustíveis e dados do levantamento de preços.

- [Série Histórica de Preços de Combustíveis e de GLP](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis)
- [Informações sobre o Levantamento de Preços](https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/precos-revenda-e-de-distribuicao-combustiveis)

Os dados são preços coletados semanalmente em postos selecionados pela pesquisa da ANP. A quantidade de observações pode variar por localidade e produto; portanto, as médias descrevem os registros disponíveis e não representam todos os postos nem são ponderadas pelo volume vendido.

## Arquivos do projeto

- `A2.py/dados/ca-2024-01.zip` e `ca-2024-02.zip`: dados brutos semestrais.
- `A2.py/a2.py`: script Python para tratamento, estatísticas e gráficos.
- `A2.py/Analise_Exploratoria_Combustiveis_2024.ipynb`: notebook Jupyter comentado com preparação, estatísticas, diagnóstico de possíveis extremos, análise temporal e regional.
- `A2.py/Esboco_Storytelling_Etapa_3.md`: narrativa e sequência dos produtos visuais da Etapa 3.
- `A2.py/relatorio/`: tabelas e base tratada geradas pelo script/notebook.
- `A2.py/graficos/`: imagens geradas pela análise.

## Como reproduzir

1. Clone ou baixe o repositório.
2. Instale Python, pandas, numpy e matplotlib.
3. Abra o notebook em `A2.py` ou na raiz do repositório e execute as células em ordem; os ZIPs são lidos diretamente.
4. Alternativamente, execute `python A2.py/a2.py` a partir da raiz. Resultados são salvos nas pastas `A2.py/relatorio` e `A2.py/graficos`.

## Autor

Adson Vinicius Galdino Passos
