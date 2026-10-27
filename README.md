# knowman site

Static site for knowman: an architecture diagram, a 6-slide deck and a landing page.
No build and no dependencies; everything publishable lives in `site/`.
View it locally: `cd site && python3 -m http.server`, then open http://localhost:8000.
Source of every fact: the `core` repo (README, CHANGELOG, `src/knowman/`).

## Languages

Three copies of the same pages, no generator and no JavaScript needed to switch:

| Language | Path |
| --- | --- |
| English (source) | `site/index.html`, `site/diagrams/`, `site/slides/` |
| Spanish | `site/es/index.html`, `site/es/diagrams/`, `site/es/slides/` |
| Portuguese (BR) | `site/pt-br/index.html`, `site/pt-br/diagrams/`, `site/pt-br/slides/` |

English is the source: change it first, then mirror the change in `es/` and `pt-br/`.
Every page carries the switcher in the header, `hreflang` alternates pointing at
`https://rdorta27.github.io/knowman-site/`, and its own `lang` attribute. The
stylesheet and the slide script are shared, so the translation folders only hold HTML.
`404.html` is English only: GitHub Pages serves that one file for any missing path.

## Publishing

GitHub Pages publishes the `site/` directory as an artifact from
`.github/workflows/pages.yml` on every push to `main` that touches it.
URL: https://rdorta27.github.io/knowman-site/
