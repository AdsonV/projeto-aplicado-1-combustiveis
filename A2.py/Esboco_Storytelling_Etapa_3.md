# Esboço do Storytelling — Etapa 3
## Projeto Aplicado I: preços de combustíveis no Brasil em 2024

### Ideia central
Em 2024, as médias observadas de gasolina comum e etanol cresceram mais entre janeiro e dezembro do que a média do diesel S10. O Norte apresentou as maiores médias regionais dos três combustíveis. A apresentação comunica esses padrões e delimita o que os dados permitem concluir.

### Pergunta central
Como os preços observados de gasolina comum, etanol hidratado e diesel S10 variaram ao longo de 2024 e entre as regiões brasileiras?

### Público e objetivo
Turma e professor do Projeto Aplicado I. Comunicar os resultados da análise exploratória com clareza, sem atribuir causas que os dados não demonstram.

### Sequência narrativa
1. **Abertura:** apresentar a pergunta e o recorte: preços de revenda coletados pela ANP em 2024 para gasolina comum, etanol hidratado e diesel S10.
2. **O que foi analisado:** explicar a fonte, a junção dos arquivos semestrais, as conversões de preço e data e o filtro dos produtos. A base tratada contém 596.594 registros: gasolina (233.020), etanol (197.306) e diesel S10 (166.268), de 1º de janeiro a 31 de dezembro.
3. **Variação durante o ano:** linha mensal. De janeiro a dezembro, as médias passaram de R$ 5,61 a R$ 6,14 na gasolina, R$ 3,70 a R$ 4,27 no etanol e R$ 5,99 a R$ 6,14 no diesel S10. Variações aproximadas: 9,4%, 15,4% e 2,5%. São médias dos registros por mês; não identificam causas.
4. **Diferenças regionais:** barras agrupadas. O Norte teve as maiores médias: R$ 6,34 (gasolina), R$ 4,60 (etanol) e R$ 6,41 (diesel S10). As menores foram R$ 5,81 (gasolina, Sudeste), R$ 3,84 (etanol, Centro-Oeste) e R$ 5,97 (diesel S10, Nordeste). Amplitudes regionais: R$ 0,53, R$ 0,76 e R$ 0,44.
5. **Interpretação responsável:** a ANP coleta preços em postos selecionados e o número de observações varia por localidade e produto. As médias representam os registros disponíveis, não são ponderadas pelo volume vendido e não garantem cobertura de todos os postos. Ler os extremos junto com as contagens.
6. **Fechamento:** neste recorte, gasolina e etanol variaram mais entre janeiro e dezembro do que o diesel S10; o Norte liderou as médias regionais. Retomar a limitação da amostra e sugerir aprofundamento por quantidade de observações locais.

### Recursos visuais

| Ordem | Visual | Mensagem |
|---|---|---|
| 1 | Linha mensal dos três combustíveis | Comparar direção e intensidade da variação em 2024. |
| 2 | Barras agrupadas por região | Mostrar diferenças e maiores médias observadas no Norte. |
| 3 | Tabela com janeiro, dezembro e variação percentual | Dar apoio numérico à conclusão temporal. |

### Recomendações
- Títulos devem resumir a mensagem e indicar métrica e período.
- Usar R$/litro, nomes regionais por extenso, cores consistentes e até duas casas decimais.
- Indicar fonte ANP e período nos gráficos ou no rodapé.
- Evitar explicações causais sem análise que as sustente.

### Rastreabilidade
Os valores foram conferidos nas tabelas versionadas em `A2.py/relatorio`. O notebook de análise pode regenerar tabelas e figuras. As médias são calculadas sobre os registros disponíveis.