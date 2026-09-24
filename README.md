# dengue_olimpia

Projeto pessoal de estudo com dado público: casos semanais de dengue em Olímpia-SP, do InfoDengue. A ideia é sair do descritivo ("quantos casos teve") pro preditivo ("quantos vão ter, e com que confiança").

A pergunta que guia o projeto: **dá pra antecipar em 2 a 4 semanas um aumento de casos de dengue em Olímpia?**

Projeto em andamento. Os resultados abaixo são só do que já está pronto.

## Dados

Série semanal do [InfoDengue](https://info.dengue.mat.br), município de Olímpia (código do Instituto Brasileiro de Geografia e Estatística (IBGE) `3533908`), de 2015 a 2025: 574 semanas epidemiológicas.

Colunas que uso:

| Coluna | O quê |
|---|---|
| `data_iniSE` | data de início da semana epidemiológica |
| `SE` | semana epidemiológica no formato `AAAASS` |
| `casos` | casos notificados na semana |
| `casos_est` | casos estimados, corrigidos pelo atraso de notificação |
| `tempmed`, `umidmed` | temperatura e umidade médias da semana |
| `nivel` | nível de alerta do InfoDengue (1 a 4) |

Pra baixar de novo:

```bash
curl -o data/raw/dengue_1-53.csv "https://info.dengue.mat.br/api/alertcity?geocode=3533908&disease=dengue&format=csv&ew_start=1&ew_end=53&ey_start=2015&ey_end=2025"
```

O InfoDengue revisa as semanas mais recentes conforme chegam notificações atrasadas, então baixar em outro dia pode dar números um pouco diferentes nas últimas semanas. O CSV vem da semana mais recente pra mais antiga, e eu ordeno por data na leitura.

## Andamento

| Etapa | Notebook | Status |
|---|---|---|
| Estatística descritiva | `notebooks/01_descritiva.ipynb` | em andamento |
| Distribuições e Teorema Central do Limite | `notebooks/02_distribuicoes_tcl.ipynb` | a fazer |
| Inferência (intervalo de confiança, testes, regressão) | `notebooks/03_inferencia.ipynb` | a fazer |
| Previsão (baselines, modelo, intervalo de previsão) | `notebooks/04_previsao.ipynb` | a fazer |
| Backtest por temporada e limitações | `src/` | a fazer |

## Primeiros achados

Da análise descritiva dos casos semanais:

- A mediana é 14 casos por semana e a média é 48,6, cerca de 3,5 vezes maior. A distribuição é bem assimétrica: a maioria das semanas tem poucos casos, e as temporadas de surto (34 semanas acima de 200 casos) puxam a média pra cima.
- Metade das semanas fica entre 5 e 42 casos (intervalo interquartil de 37).
- O desvio padrão (92,1) é quase o dobro da média. A faixa média ± 1 desvio vai de -43,5 a 140,8 casos: pega 91% das semanas, contra os ~68% esperados numa distribuição normal, e o limite de baixo nem é possível. Por isso descrevo a série com mediana e intervalo interquartil, e não com média ± desvio.
- Semana de surto não é tratada como outlier a descartar. O surto é justamente o que o projeto quer prever.

## Limitações conhecidas

- **Subnotificação:** nem todo caso de dengue é notificado, então `casos` fica abaixo do número real.
- **Dado revisado depois:** as semanas recentes ainda mudam. Qualquer coluna que só fica pronta depois da semana acabar não pode entrar como variável de previsão.
- **Notificados ou estimados:** ainda preciso decidir se o alvo do modelo é `casos` ou `casos_est`. Por enquanto a análise descritiva usa `casos`.

## Estrutura

```
dengue_olimpia/
├── data/
│   ├── raw/          # dado original, nunca editado (fora do git)
│   ├── processed/    # dado limpo, pronto pra modelar
│   └── external/     # dado de outras fontes
├── notebooks/        # exploração e análise
├── sql/              # queries
├── src/              # funções reaproveitadas pelos notebooks
│   ├── data/
│   ├── features/
│   ├── models/
│   └── visualization/
└── reports/
    └── figures/      # gráficos
```

`src/` é instalado no ambiente do projeto, então os notebooks importam direto (`from src.features import ...`).

## Como rodar

Precisa do [uv](https://docs.astral.sh/uv/).

```bash
uv sync
# baixar o CSV (comando da seção Dados)
uv run jupyter lab
```

Ou abrir a pasta no VS Code e escolher o kernel do `.venv` do projeto.

Os dados são públicos, do InfoDengue. Este é um projeto pessoal e não representa nenhum órgão público.
