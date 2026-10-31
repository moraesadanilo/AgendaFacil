# AgendaFácil

Agenda de atendimentos de uma clínica pequena: marca, remarca, cancela e
lista atendimentos em memória.  
Projeto desenvolvido para disciplina Boas Práticas de Programação (DIMAp/UFRN).
Este projeto foi refatorado a partir de um código legado, aplicando princípios de modularidade, programação defensiva e documentação em padrão Google.

## Requisitos

- Python 3.10 ou superior
- O sistema usa apenas a biblioteca padrão. A única ferramenta externa é o
  `pdoc`, necessária somente para gerar a documentação.
- Gerenciador de pacotes uv para isolamento do ambiente virtual (Opcional).

## Estrutura

| Arquivo | Responsabilidade |
|---|---|
| `agendamento.py` | Regras de negócio. Valida e levanta exceções; não imprime. |
| `interface.py` | Apresentação no console. Captura `AgendaError` e imprime. |
| `agenda_app.py` | Programa de demonstração. |
| `docs/` | Documentação de API gerada (abra `docs/index.html`). |

## Como executar

```bash
python agenda_app.py
```

## Como gerar a documentação
A documentação do sistema foi gerada utilizando a biblioteca pdoc. Os arquivos finais em HTML encontram-se na pasta docs/.


```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install pdoc
python -m pdoc agendamento interface -o docs --docformat google
```

Depois, abra `docs/index.html` no navegador.  
Dê dois cliques em index.html se ele abrir como um editor de texto, clique com o botão direito, escolha Abrir com e selecione o navegador.

Alternativa com uv:

```bash
uv venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
uv pip install pdoc  
python -m pdoc agendamento interface -o docs --docformat google
```

## Autor

- Danilo Araujon de Moraes — 20250067023
