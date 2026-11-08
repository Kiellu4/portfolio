#!/usr/bin/env python3
"""Render pretty static write-up pages from content/writeups JSON files."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "writeups"
OUTPUT = ROOT / "writeups"


def e(value: object) -> str:
    return html.escape(str(value), quote=True)


def site_nav() -> str:
    pages = [("I", "Whoami", "whoami"), ("II", "About", "about"), ("III", "Experience", "experience"), ("IV", "Projects", "projects"), ("V", "Achievements", "achievements"), ("VI", "Write-ups", "writeups"), ("VII", "Licenses", "certifications"), ("VIII", "Contact", "contact")]
    links = "\n".join(f'          <a href="../index.html#{anchor}">{roman} <span>{label}</span></a>' for roman, label, anchor in pages)
    return f'''    <header class="site-header">
      <nav class="nav container" aria-label="Primary navigation">
        <a class="brand" href="../index.html#whoami" aria-label="Kiel home">KIEL<span>_</span></a>
        <button class="menu-button" type="button" aria-expanded="false" aria-controls="nav-links"><span class="sr-only">Toggle navigation</span><span></span><span></span><span></span></button>
        <div class="nav-links" id="nav-links">
{links}
          <button class="theme-toggle" type="button" aria-label="Switch to light theme">☼</button>
        </div>
      </nav>
    </header>'''


def challenge_card(item: dict) -> str:
    meta = " · ".join(e(value) for value in (item.get("category"), item.get("points"), item.get("difficulty")) if value)
    solver = e(item["solver"])
    step_markup = []
    for step in item.get("steps", []):
        paragraphs = "\n".join(f"                <p>{e(paragraph)}</p>" for paragraph in step.get("text", []))
        code = "\n".join(f'                <p class="code-language">{e(block.get("lang", "text"))}</p>\n                <pre><code>{e(block["text"])}</code></pre>' for block in step.get("code", []))
        images = "\n".join(f'                <figure><img class="writeup-figure" src="../{e(pic["src"])}" alt="{e(pic["alt"])}" loading="lazy"><figcaption>{e(pic["caption"])}</figcaption></figure>' for pic in step.get("images", []))
        files = "\n".join(f'                <a class="file-download" href="../{e(file["path"])}" download>{e(file["label"])}<span>{e(file.get("size", ""))}</span></a>' for file in step.get("files", []))
        step_markup.append(f'''              <li class="solve-step"><h4>{e(step["title"])}</h4>
{paragraphs}
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
    for source in sorted(CONTENT.glob("*.json")):
        data = json.loads(source.read_text(encoding="utf-8"))
        target = OUTPUT / data["output"]
        target.write_text(render(data), encoding="utf-8")
        print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
