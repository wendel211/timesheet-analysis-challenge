# Timesheet Analysis Challenge

Aplicacao containerizada em Python para processar registros de timesheet a partir de `data.json` e gerar um resumo analitico em `result.json`.

## Requisitos atendidos

- Leitura local do arquivo `data.json`.
- Ignora registros com `minutes <= 0`.
- Conta registros ignorados em `ignoredRecords`.
- Agrupa minutos por tarefa.
- Identifica a tarefa mais trabalhada.
- Calcula percentual por tarefa com duas casas decimais.
- Retorna top 3 tarefas por percentual.
- Retorna top 3 funcionarios por total de minutos.
- Identifica o usuario com mais tarefas distintas.
- Gera saida deterministica seguindo as regras de ordenacao do desafio.
- Executa exclusivamente via Docker Compose.

## Como executar

```bash
docker compose up --build
```

Ao final da execucao, o arquivo `result.json` sera criado na raiz do projeto.

## Como validar localmente

Executar a aplicacao:

```bash
python src/main.py
```

Rodar os testes:

```bash
python -m unittest discover -s tests -v
```

Os testes comparam o resultado gerado pela regra de negocio com o gabarito `output.json` e tambem cobrem os principais criterios de desempate.

## Estrutura

```text
.
├── data.json
├── output.json
├── Dockerfile
├── docker-compose.yml
├── src
│   ├── main.py
│   └── timesheet_analysis.py
└── tests
    └── test_timesheet_analysis.py
```

## Decisoes tecnicas

- Python puro, usando apenas a biblioteca padrao.
- Sem dependencias externas, banco de dados ou chamadas de rede.
- Logica de negocio separada do ponto de entrada para facilitar testes.
- `output.json` e usado apenas como fixture de validacao; a aplicacao nao depende dele.
- `result.json` e um artefato gerado e nao deve ser versionado.
