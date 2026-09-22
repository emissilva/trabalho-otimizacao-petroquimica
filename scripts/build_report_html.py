"""Gera o relatório HTML a partir do Markdown canônico."""

from pathlib import Path

import markdown


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "relatorio" / "relatorio.md"
OUTPUT = ROOT / "relatorio" / "relatorio.html"

MEMBERS = [
    ("Elton Vinicios Almeida de Oliveira", "RM 562187"),
    ("Emerson dos Santos Silva", "RM 562033"),
    ("Kelvin Douglas Ribeiro Rabelo", "RM 561538"),
    ("Pedro Henrique Simão Soares", "RM 562283"),
    ("Vitor Lucas Mattos de Brito Mariano", "RM 562116"),
]


def build() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    body_source = "## 1. Entendimento do negócio" + source.split(
        "## 1. Entendimento do negócio", 1
    )[1]
    body = markdown.markdown(
        body_source,
        extensions=["tables", "fenced_code", "toc", "sane_lists"],
        output_format="html5",
    )
    members = "".join(
        f'<li><span>{name}</span><strong>{rm}</strong></li>' for name, rm in MEMBERS
    )
    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Relatório — Pipeline de ML, Otimização e Manutenção</title>
<style>
@font-face{{font-family:Inter;src:url('../fontes/Inter-Regular.ttf')}}
@font-face{{font-family:Inter;src:url('../fontes/Inter-Bold.ttf');font-weight:700}}
:root{{--ink:#182033;--muted:#647080;--accent:#d51f3d;--teal:#087f87;--line:#dfe3e8;--soft:#f4f5f7;--paper:#fff}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:#edf0f3;color:var(--ink);font-family:Inter,Arial,sans-serif;line-height:1.58}}
.page{{width:min(1120px,calc(100% - 32px));margin:28px auto;background:var(--paper);box-shadow:0 12px 40px rgba(20,28,40,.10)}}
.cover{{min-height:720px;padding:80px 78px;display:grid;grid-template-columns:1.2fr .8fr;gap:58px;align-items:center;border-top:7px solid var(--accent)}}
.eyebrow{{color:var(--accent);font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}}h1{{font-size:48px;line-height:1.08;letter-spacing:-.04em;margin:18px 0}}.lead{{font-size:19px;color:var(--muted);max-width:650px}}.meta{{margin-top:35px;color:var(--muted);font-size:13px}}
.team{{background:var(--soft);border:1px solid var(--line);border-left:4px solid var(--accent);padding:26px}}.team h2{{margin:0 0 15px;font-size:20px}}.team ul{{list-style:none;padding:0;margin:0}}.team li{{padding:10px 0;border-top:1px solid var(--line);font-size:12px}}.team li span,.team li strong{{display:block}}.team li strong{{color:var(--accent);margin-top:2px}}
main{{padding:60px 78px 90px}}h2{{font-size:28px;margin:52px 0 18px;padding-bottom:10px;border-bottom:2px solid var(--accent);letter-spacing:-.025em}}h3{{font-size:20px;margin:34px 0 12px;color:var(--teal)}}p,li{{font-size:14px}}code{{background:#eef0f3;padding:2px 5px;border-radius:4px}}pre{{background:#182033;color:#f6f7f9;padding:20px;border-radius:8px;overflow:auto;line-height:1.45}}
table{{border-collapse:collapse;width:100%;margin:18px 0 28px;font-size:12px;display:block;overflow-x:auto}}th{{background:#182033;color:#fff;text-align:left}}th,td{{border:1px solid var(--line);padding:9px 10px;vertical-align:top}}tbody tr:nth-child(even){{background:#f7f8f9}}blockquote{{margin:20px 0;padding:12px 18px;border-left:4px solid var(--accent);background:#fff4f5;color:var(--muted)}}strong{{font-weight:700}}
@media(max-width:800px){{.cover{{grid-template-columns:1fr;padding:48px 34px}}h1{{font-size:36px}}main{{padding:40px 28px}}}}
@media print{{body{{background:#fff}}.page{{width:100%;margin:0;box-shadow:none}}.cover{{page-break-after:always}}main{{padding:30px 42px}}h2,h3{{page-break-after:avoid}}table,pre{{page-break-inside:avoid}}}}
</style>
</head>
<body><div class="page">
<header class="cover">
  <div><div class="eyebrow">FIAP · Machine Learning + Otimização</div>
  <h1>Pipeline de ML, Otimização e Decisão de Manutenção</h1>
  <p class="lead">Relatório técnico do processo petroquímico: entendimento do negócio, modelos preditivos, otimização operacional, cenários de manutenção e recomendação de automação.</p>
  <p class="meta"><b>Dataset:</b> petrochemical_advanced_data.csv · 10.000 registros · 2020–2024<br><b>Turma:</b> 2TSCPW · <b>Ano:</b> 2026</p></div>
  <aside class="team"><h2>Equipe Predictfy</h2><ul>{members}</ul></aside>
</header>
<main>{body}</main>
</div></body></html>"""
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"HTML criado: {OUTPUT}")


if __name__ == "__main__":
    build()
