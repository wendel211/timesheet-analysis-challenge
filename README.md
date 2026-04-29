# Timesheet Analysis Challenge

Solucao containerizada em Python para processar registros de timesheet a partir de `data.json` e gerar um resumo analitico deterministico em `result.json`.

O projeto foi desenvolvido para o desafio tecnico, com foco em manipulacao de dados, regras de negocio, tratamento de entradas invalidas, ordenacao deterministica e execucao via Docker.

## Sumario

- [Execucao com Docker](#execucao-com-docker)
- [Resultado gerado](#resultado-gerado)
- [Validacao local](#validacao-local)
- [Regras implementadas](#regras-implementadas)
- [Ordenacao deterministica](#ordenacao-deterministica)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Decisoes tecnicas](#decisoes-tecnicas)
- [Tratamento de erros](#tratamento-de-erros)

## Execucao com Docker

Com Docker e Docker Compose instalados, execute na raiz do projeto:

```bash
docker compose up --build
```

Ao final da execucao, a aplicacao cria o arquivo:

```text
result.json
```

Esse arquivo e gerado localmente na raiz do projeto por meio do volume configurado no `docker-compose.yml`.

## Resultado gerado

A saida segue a estrutura solicitada no desafio:

```json
{
  "totalMinutes": 28408,
  "tasks": [],
  "mostWorkedTask": {},
  "top3TasksPercentage": [],
  "top3Employees": [],
  "mostDistinctUserOnTasks": {},
  "ignoredRecords": 41
}
```

Campos principais:

- `totalMinutes`: soma total de minutos considerando apenas registros validos.
- `tasks`: lista de tarefas agrupadas por `taskId`, com total de minutos e percentual.
- `mostWorkedTask`: tarefa com maior total de minutos.
- `top3TasksPercentage`: tres tarefas com maior volume de minutos e seus percentuais.
- `top3Employees`: tres usuarios com maior total de minutos trabalhados.
- `mostDistinctUserOnTasks`: usuario que trabalhou na maior quantidade de tarefas distintas.
- `ignoredRecords`: quantidade de registros ignorados por terem `minutes <= 0`.

## Validacao local

Executar a aplicacao sem Docker:

```bash
python src/main.py
```

Rodar a suite de testes:

```bash
python -m unittest discover -s tests -v
```

Comparar `result.json` com o gabarito `output.json`:

```bash
python -c "import json; print(json.load(open('result.json', encoding='utf-8')) == json.load(open('output.json', encoding='utf-8')))"
```

O resultado esperado da comparacao e:

```text
True
```

## Regras implementadas

A aplicacao:

- Le o arquivo local `data.json`.
- Valida se o input principal e uma lista de registros.
- Ignora registros com `minutes <= 0`.
- Conta os registros ignorados em `ignoredRecords`.
- Agrupa tarefas por `taskId`.
- Soma o total de minutos por tarefa.
- Calcula o percentual de cada tarefa sobre o total geral.
- Formata percentuais com duas casas decimais e sufixo `%`.
- Identifica a tarefa mais trabalhada.
- Retorna o top 3 de tarefas.
- Agrupa usuarios por `userId`.
- Soma o total de minutos por usuario.
- Retorna o top 3 de funcionarios.
- Identifica o usuario com mais tarefas distintas.
- Ordena `taskIds` do usuario com mais tarefas distintas em ordem crescente.

## Ordenacao deterministica

Para garantir que a saida seja sempre reproduzivel, as ordenacoes seguem exatamente as regras do desafio:

Tarefas:

1. `totalMinutes` em ordem decrescente.
2. `taskId` em ordem crescente em caso de empate.

Funcionarios:

1. `totalMinutes` em ordem decrescente.
2. `userId` em ordem crescente em caso de empate.

Usuario com mais tarefas distintas:

1. `distinctTasks` em ordem decrescente.
2. `userId` em ordem crescente em caso de empate.

## Estrutura do projeto

```text
.
|-- .dockerignore
|-- .gitignore
|-- Dockerfile
|-- README.md
|-- data.json
|-- docker-compose.yml
|-- output.json
|-- src
|   |-- __init__.py
|   |-- main.py
|   `-- timesheet_analysis.py
`-- tests
    |-- __init__.py
    `-- test_timesheet_analysis.py
```

Responsabilidades:

- `src/main.py`: ponto de entrada da aplicacao.
- `src/timesheet_analysis.py`: regras de negocio, validacao, agregacoes e escrita do resultado.
- `tests/test_timesheet_analysis.py`: testes automatizados das regras principais e comparacao com o gabarito.
- `data.json`: dataset de entrada.
- `output.json`: gabarito usado somente para validacao.
- `result.json`: artefato gerado em runtime e ignorado pelo Git.

## Decisoes tecnicas

- Python puro com biblioteca padrao.
- Sem dependencias externas.
- Sem banco de dados.
- Sem chamadas HTTP ou acesso a rede.
- Execucao principal via Docker Compose.
- Logica de negocio separada do ponto de entrada para facilitar teste e manutencao.
- Saida JSON com campos em ordem estavel.
- `output.json` nao e usado pela aplicacao, apenas pelos testes.
- `result.json` nao e versionado, pois deve ser produzido ao executar o projeto.

## Tratamento de erros

A aplicacao falha com mensagem clara quando:

- `data.json` nao existe.
- `data.json` nao contem JSON valido.
- O conteudo principal nao e uma lista.
- Um registro valido nao possui campos obrigatorios.
- Campos numericos essenciais, como `minutes`, `userId` ou `taskId`, possuem tipos invalidos.

Registros com `minutes <= 0` nao sao tratados como erro, pois a regra do desafio determina que eles devem ser ignorados e contabilizados.

## Complexidade

Considerando `n` registros validos, `t` tarefas distintas e `u` usuarios distintos:

- Processamento dos registros: `O(n)`.
- Ordenacao de tarefas: `O(t log t)`.
- Ordenacao de usuarios: `O(u log u)`.
- Uso de memoria: `O(t + u)`.

## Checklist rapido

- [x] Leitura local de `data.json`.
- [x] Geracao de `result.json`.
- [x] Ignora `minutes <= 0`.
- [x] Contabiliza `ignoredRecords`.
- [x] Calcula totais por tarefa.
- [x] Calcula percentuais com duas casas.
- [x] Retorna top 3 tarefas.
- [x] Retorna top 3 funcionarios.
- [x] Identifica usuario com mais tarefas distintas.
- [x] Aplica criterios de desempate.
- [x] Executa com `docker compose up --build`.
- [x] Inclui testes automatizados.
- [x] Compara resultado com `output.json`.
