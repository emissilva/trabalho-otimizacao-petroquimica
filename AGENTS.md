# Instruções locais do projeto

Antes de modificar qualquer entregável, leia `REQUISITOS_DO_TRABALHO.md` e confira o checklist do professor. Preserve a distinção entre resultados reproduzidos, premissas didáticas e limitações.

## Política obrigatória de ambientes Python

- Use exclusivamente `uv` para desenvolvimento, execução, testes, notebooks, artefatos e dependências Python.
- Use interpretadores gerenciados pelo uv e ambientes `.venv`; nunca use ou instale Python ou pacotes globalmente para atender projetos.
- Em projetos com `pyproject.toml` e `uv.lock`, use `uv sync --locked` e `uv run --project <pasta> python ...`. Prefira `uv add` e mantenha os arquivos reproduzíveis atualizados.
- Para estudos avulsos, use `~/python-envs/deep` em ML/deep learning e `~/python-envs/dev` em desenvolvimento geral; execute com `uv run --project "$HOME/python-envs/<ambiente>" ...`.
- Não dependa apenas da ativação do shell. Não use `uv pip --system`, `sudo pip`, `pip install --user`, Python do macOS/Homebrew ou instalação global como solução.
- Use `uv pip` somente em casos excepcionais com `--python` apontando explicitamente para a `.venv`; registre dependências no manifesto e no lock.
- No Mac M4, use Python e bibliotecas ARM64. PyTorch usa MPS; TensorFlow usa Metal quando a combinação de versões é compatível. Não instale CUDA para a GPU Apple nem prometa aceleração de bibliotecas que só suportam CPU nessa plataforma.
- Preserve todos os frameworks necessários; informe bibliotecas incompatíveis, versões e causas antes de descartar funcionalidades.
- Crie uma `.venv` própria para projetos com requisitos conflitantes. Não altere ou remova ambientes compartilhados sem avaliar o impacto.
- Instalações Python de outras ferramentas e do sistema não pertencem aos projetos e não devem ser removidas como limpeza de ambiente.
- Ao finalizar trabalho com um novo ambiente específico, informe seu caminho e pergunte se o usuário deseja mantê-lo ou removê-lo; não o remova automaticamente.

