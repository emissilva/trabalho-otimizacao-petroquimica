# Trabalho de otimização petroquímica

Pipeline acadêmico completo de dados, Machine Learning, otimização, cenários e decisão de manutenção.

Antes de alterar os entregáveis, consulte `REQUISITOS_DO_TRABALHO.md` e `AUDITORIA_FINAL.md`.

## Estrutura

- `data/`: dataset original;
- `notebook/`: pipeline executável e com saídas reproduzidas;
- `relatorio/`: relatório Markdown, HTML e PDF sincronizados;
- `apresentacao/`: HTML, PDF, PowerPoint e roteiro didático para 14 a 15 minutos;
- `fontes/`: arquivos Inter usados no HTML e incorporados ao PPTX;
- `scripts/`: geração reproduzível do notebook, relatório, HTML e PPTX;
- `originais/`: pacote recebido, preservado sem alterações.

## Execução

```bash
uv sync --locked
uv run --project . python scripts/build_notebook.py
uv run --project . python scripts/execute_notebook.py
uv run --project . python scripts/build_artifacts.py
uv run --project . python scripts/build_report_html.py
# Requer Playwright/Chromium para imprimir o HTML em PDF:
NODE_PATH=/private/tmp/petro-html/node_modules node scripts/render_presentation_html.cjs
uv run --project . python scripts/build_presentation_pptx_from_pdf.py
```

A apresentação visual em modo claro tem como fonte canônica [apresentacao.html](apresentacao/apresentacao.html). O PDF é renderizado pelo Chromium com fontes locais; o PPTX usa as páginas renderizadas para preservar exatamente o mesmo layout.

O notebook usa caminhos relativos e deve ser executado a partir deste projeto. As dependências e a versão compatível do Python estão declaradas em `pyproject.toml`, permitindo que o projeto seja preparado com o gerenciador de ambientes disponível no local de execução.
