#!/usr/bin/env python3
"""Render pretty static write-up pages from content/writeups JSON files."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "writeups"
OUTPUT = ROOT / "writeups"
CARD_VCF = """BEGIN:VCARD
VERSION:3.0
FN:Ezekiel Mukhriz
TITLE:System Engineer
ORG:MyOne Corporation
EMAIL:ezekiel@myonecorp.com
URL:https://kiellu4.github.io/portfolio/
ADR:;;Unit 19-3\\, Block C1 Dataran Prima\\, Jalan PJU 1/41;Petaling Jaya;Selangor;47301;Malaysia
SOCIAL;type=linkedin:https://www.linkedin.com/in/ezekiel-mukhriz
SOCIAL;type=github:https://github.com/Kiellu4
END:VCARD
"""


def e(value: object) -> str:
    return html.escape(str(value), quote=True)


def site_nav() -> str:
    pages = [("I", "whoami", "whoami"), ("II", "about", "about"), ("III", "experience", "experience"), ("IV", "projects", "projects"), ("V", "Achievements", "achievements"), ("VI", "CTF Write-ups", "writeups"), ("VII", "Licenses &amp; certifications", "certifications"), ("VIII", "contact", "contact")]
    links = "\n".join(
        f'          <a href="../index.html#{anchor}"><span class="nav-roman">{roman}</span><span class="nav-label">: {label}</span></a>'
        for roman, label, anchor in pages
    )
    return f'''    <header class="site-header">
      <nav class="nav container" aria-label="Primary navigation">
        <button class="menu-button" type="button" aria-expanded="false" aria-controls="nav-links"><span class="sr-only">Toggle navigation</span><span></span><span></span><span></span></button>
        <div class="nav-middle">
        <div class="nav-links nav-main" id="nav-links">
          <span class="brand" aria-label="Kiel">K</span>
{links}
        </div>
        <div class="nav-widgets">
          <button class="theme-toggle" type="button" aria-label="Switch to light theme">☼</button>
          <span class="status-working"><span class="status-dot" aria-hidden="true"></span>working</span>
          <a class="status-icon" href="https://github.com/Kiellu4" target="_blank" rel="noopener" aria-label="GitHub profile"><svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M12 2C6.48 2 2 6.58 2 12.23c0 4.52 2.87 8.35 6.84 9.7.5.1.68-.22.68-.49 0-.24-.01-1.04-.01-1.89-2.78.62-3.37-1.2-3.37-1.2-.45-1.19-1.11-1.5-1.11-1.5-.91-.64.07-.63.07-.63 1 .07 1.53 1.06 1.53 1.06.9 1.57 2.35 1.12 2.92.85.09-.67.35-1.12.64-1.38-2.22-.26-4.56-1.14-4.56-5.07 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.31.1-2.73 0 0 .84-.28 2.75 1.05A9.23 9.23 0 0 1 12 6.9c.85 0 1.7.12 2.5.35 1.91-1.33 2.75-1.05 2.75-1.05.55 1.42.2 2.47.1 2.73.64.72 1.03 1.63 1.03 2.75 0 3.94-2.35 4.8-4.58 5.06.36.32.68.92.68 1.85 0 1.34-.01 2.42-.01 2.75 0 .27.18.6.69.49A10.25 10.25 0 0 0 22 12.23C22 6.58 17.52 2 12 2Z" fill="currentColor"/></svg></a>
          <a class="status-icon" href="mailto:mukhrizfitry@gmail.com" aria-label="Email Muhammad Ezekiel Mukhriz"><svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="3" y="4.5" width="18" height="15" rx="2" stroke="currentColor" stroke-width="1.7"/><path d="m4.5 6 7.5 5.8L19.5 6" stroke="currentColor" stroke-width="1.7"/></svg></a>
          <div class="nav-clock" aria-label="Local time"><span>--:--:--</span><small>--/--/--</small></div>
        </div>
        </div>
      </nav>
    </header>'''


def challenge_card(item: dict) -> str:
    if item.get("title_only"):
        return f'''          <details class="challenge-card">
            <summary><span><strong>{e(item["title"])}</strong></span><span aria-hidden="true">+</span></summary>
          </details>'''
    meta = " · ".join(e(value) for value in (item.get("category"), item.get("points"), item.get("difficulty")) if value)
    solver = e(item["solver"])
    step_markup = []
    for step in item.get("steps", []):
        paragraphs = "\n".join(f"                <p>{e(paragraph)}</p>" for paragraph in step.get("text", []))
        tables = "\n".join(
            "                <div class=\"table-wrap\"><table><thead><tr>"
            + "".join(f"<th>{e(cell)}</th>" for cell in table.get("headers", []))
            + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{e(cell)}</td>" for cell in row) + "</tr>" for row in table.get("rows", []))
            + "</tbody></table></div>"
            for table in step.get("tables", [])
        )
        code = "\n".join(f'                <p class="code-language">{e(block.get("lang", "text"))}</p>\n                <pre><code>{e(block["text"])}</code></pre>' for block in step.get("code", []))
        images = "\n".join(f'                <figure><img class="writeup-figure" src="../{e(pic["src"])}" alt="{e(pic["alt"])}" loading="lazy"><figcaption>{e(pic["caption"])}</figcaption></figure>' for pic in step.get("images", []))
        files = "\n".join(f'                <a class="file-download" href="../{e(file["path"])}" download>{e(file["label"])}<span>{e(file.get("size", ""))}</span></a>' for file in step.get("files", []))
        step_markup.append(f'''              <li class="solve-step"><h4>{e(step["title"])}</h4>
{paragraphs}
{tables}
{code}
{images}
{files}
              </li>''')
    steps = "\n".join(step_markup) or "              <li>Write-up pending: no source steps have been entered yet.</li>"
    challenge_files = "\n".join(
        f'              <a class="file-download" href="../{e(file["path"])}" download>{e(file["label"])}<span>{e(file.get("size", ""))}</span></a>'
        for file in item.get("files", [])
    )
    flag = f'            <p class="flag-label">Flag</p>\n            <pre><code>{e(item["flag"])}</code></pre>' if item.get("flag") else ""
    return f'''          <details class="challenge-card">
            <summary><span><span class="mono-label">{meta}</span><strong>{e(item["title"])}</strong></span><span aria-hidden="true">+</span></summary>
            <div class="challenge-body">
              <span class="team-credit">Solved by: {solver}</span>
              <h4>Challenge</h4><p>{e(item.get("overview", "Write-up pending."))}</p>
              <h4>First look / analysis</h4><p>{e(item.get("analysis", "No analysis was recorded."))}</p>
              <ol>
{steps}
              </ol>
              <h4>Result</h4><p>{e(item.get("result", "No result was recorded."))}</p>
{flag}
{challenge_files}
              <p><strong>Tools used:</strong> {e(item.get("tools", "TODO"))}. <strong>What I learned:</strong> {e(item.get("learned", "TODO"))}</p>
            </div>
          </details>'''


def render(data: dict) -> str:
    categories = data.get("categories", [])
    toc = "\n".join(f'          <a href="#{e(category["slug"])}">{e(category["name"])}</a>' for category in categories)
    sections = "\n".join(f'''      <section class="writeup-category" id="{e(category["slug"])}">
        <h2>{e(category["name"])}</h2>
        <div class="challenge-list">
{chr(10).join(challenge_card(item) for item in category.get("challenges", []))}
        </div>
      </section>''' for category in categories)
    tags = "".join(f"<li>{e(tag)}</li>" for tag in data.get("tags", []))
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{e(data["event"])} CTF write-ups by Muhammad Ezekiel Mukhriz and permitted teammates.">
    <meta name="theme-color" content="#080c10">
    <meta property="og:title" content="{e(data["event"])} Write-ups | Muhammad Ezekiel Mukhriz">
    <meta property="og:type" content="website">
    <meta property="og:image" content="../{e(data["cover"])}">
    <title>{e(data["event"])} Write-ups | Muhammad Ezekiel Mukhriz</title>
    <link rel="icon" href="../favicon.svg" type="image/svg+xml">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=JetBrains+Mono:wght@500;600;700&amp;display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../styles.css">
  </head>
  <body>
    <a class="skip-link" href="#main-content">Skip to content</a>
{site_nav()}
    <main id="main-content" class="writeup-page"><div class="container">
      <a class="back-link" href="../index.html#writeups">← Back to CTF write-ups</a>
      <section class="writeup-hero"><div><p class="mono-label">{e(data["event"])}</p><h1>{e(data["result"])}</h1><p>{e(data["team"])}</p><p>{e(data.get("members", ""))}</p><ul class="tags">{tags}</ul></div><img src="../{e(data["cover"])}" alt="{e(data["event"])} event cover" loading="lazy"></section>
      <p class="redaction-note">{e(data.get("note_label", "Note"))}: {e(data.get("note", "Published after the competition ended."))}</p>
      <nav class="writeup-toc" aria-label="Write-up contents"><p class="mono-label">ON THIS PAGE</p>
{toc}
      </nav>
{sections}
    </div></main>
    <footer><div class="container"><p>© <span id="year"></span> Muhammad Ezekiel Mukhriz.</p><p>built by hand, deployed to GitHub Pages</p></div></footer>
    <script src="../script.js"></script>
  </body>
</html>
'''


def main() -> None:
    (ROOT / "assets" / "card.vcf").write_text(CARD_VCF, encoding="utf-8")
    for source in sorted(CONTENT.glob("*.json")):
        data = json.loads(source.read_text(encoding="utf-8"))
        target = OUTPUT / data["output"]
        target.write_text(render(data), encoding="utf-8")
        print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
