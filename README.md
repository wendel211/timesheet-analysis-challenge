# Timesheet Analysis Challenge

Solução containerizada em Python para processar registros de timesheet a partir de `data.json` e gerar um resumo analítico determinístico em `result.json`.

O projeto foi desenvolvido para o desafio técnico, com foco em manipulação de dados, regras de negócio, tratamento de entradas inválidas, ordenação determinística e execução via Docker.

## Sumário

- [Execução com Docker](#execucao-com-docker)
- [Resultado gerado](#resultado-gerado)
- [Validação local](#validacao-local)
- [Regras implementadas](#regras-implementadas)
- [Ordenação determinística](#ordenacao-deterministica)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Decisões técnicas](#decisoes-tecnicas)
- [Tratamento de erros](#tratamento-de-erros)

## Execução com Docker

Com Docker e Docker Compose instalados, execute na raiz do projeto:

```bash
docker compose up --build
```

Ao final da execução, a aplicação cria o arquivo:

```text
result.json
```

Esse arquivo é gerado localmente na raiz do projeto por meio do volume configurado no `docker-compose.yml`.

## Resultado gerado

A saída segue a estrutura solicitada no desafio:

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

- `totalMinutes`: soma total de minutos considerando apenas registros válidos.
- `tasks`: lista de tarefas agrupadas por `taskId`, com total de minutos e percentual.
- `mostWorkedTask`: tarefa com maior total de minutos.
- `top3TasksPercentage`: três tarefas com maior volume de minutos e seus percentuais.
- `top3Employees`: três usuários com maior total de minutos trabalhados.
- `mostDistinctUserOnTasks`: usuário que trabalhou na maior quantidade de tarefas distintas.
- `ignoredRecords`: quantidade de registros ignorados por terem `minutes <= 0`.

## Validação local

Executar a aplicação sem Docker:

```bash
python src/main.py
```

Rodar a suíte de testes:

```bash
python -m unittest discover -s tests -v
```

Comparar `result.json` com o gabarito `output.json`:

```bash
python -c "import json; print(json.load(open('result.json', encoding='utf-8')) == json.load(open('output.json', encoding='utf-8')))"
```

O resultado esperado da comparação é:

```text
True
```

## Regras implementadas

A aplicação:

- Lê o arquivo local `data.json`.
- Valida se o input principal é uma lista de registros.
- Ignora registros com `minutes <= 0`.
- Conta os registros ignorados em `ignoredRecords`.
- Agrupa tarefas por `taskId`.
- Soma o total de minutos por tarefa.
- Calcula o percentual de cada tarefa sobre o total geral.
- Formata percentuais com duas casas decimais e sufixo `%`.
- Identifica a tarefa mais trabalhada.
- Retorna o top 3 de tarefas.
- Agrupa usuários por `userId`.
- Soma o total de minutos por usuário.
- Retorna o top 3 de funcionários.
- Identifica o usuário com mais tarefas distintas.
- Ordena `taskIds` do usuário com mais tarefas distintas em ordem crescente.

## Ordenação determinística

Para garantir que a saída seja sempre reproduzível, as ordenações seguem exatamente as regras do desafio:

Tarefas:

1. `totalMinutes` em ordem decrescente.
2. `taskId` em ordem crescente em caso de empate.

Funcionários:

1. `totalMinutes` em ordem decrescente.
2. `userId` em ordem crescente em caso de empate.

Usuário com mais tarefas distintas:

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

- `src/main.py`: ponto de entrada da aplicação.
- `src/timesheet_analysis.py`: regras de negócio, validação, agregações e escrita do resultado.
- `tests/test_timesheet_analysis.py`: testes automatizados das regras principais e comparação com o gabarito.
- `data.json`: dataset de entrada.
- `output.json`: gabarito usado somente para validação.
- `result.json`: artefato gerado em runtime e ignorado pelo Git.

## Decisões técnicas

- Python puro com biblioteca padrão.
- Sem dependências externas.
- Sem banco de dados.
- Sem chamadas HTTP ou acesso à rede.
- Execução principal via Docker Compose.
- Lógica de negócio separada do ponto de entrada para facilitar teste e manutenção.
- Saída JSON com campos em ordem estável.
- `output.json` não é usado pela aplicação, apenas pelos testes.
- `result.json` não é versionado, pois deve ser produzido ao executar o projeto.

## Tratamento de erros

A aplicação falha com mensagem clara quando:

- `data.json` não existe.
- `data.json` não contém JSON válido.
- O conteúdo principal não é uma lista.
- Um registro válido não possui campos obrigatórios.
- Campos numéricos essenciais, como `minutes`, `userId` ou `taskId`, possuem tipos inválidos.

Registros com `minutes <= 0` não são tratados como erro, pois a regra do desafio determina que eles devem ser ignorados e contabilizados.

## Complexidade

Considerando `n` registros válidos, `t` tarefas distintas e `u` usuários distintos:

- Processamento dos registros: `O(n)`.
- Ordenação de tarefas: `O(t log t)`.
- Ordenação de usuários: `O(u log u)`.
- Uso de memória: `O(t + u)`.

## Checklist rápido

- [x] Leitura local de `data.json`.
- [x] Geração de `result.json`.
- [x] Ignora `minutes <= 0`.
- [x] Contabiliza `ignoredRecords`.
- [x] Calcula totais por tarefa.
- [x] Calcula percentuais com duas casas.
- [x] Retorna top 3 tarefas.
- [x] Retorna top 3 funcionários.
- [x] Identifica usuário com mais tarefas distintas.
- [x] Aplica critérios de desempate.
- [x] Executa com `docker compose up --build`.
- [x] Inclui testes automatizados.
- [x] Compara resultado com `output.json`.
