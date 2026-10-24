---
name: anki.math
description: MathJax (\(...\), \[...\]) and LaTeX ([latex]...[/latex], [$]...[/$], [$$]...[/$$]) in Anki cards, mhchem chemistry, and the known conflicts between cloze/LaTeX delimiters and template field replacements. Use when adding equations or chemical notation to Anki cards.
---

# Anki Math & Symbols

Two engines: **MathJax** (recommended, no install) and **LaTeX** (image
generation, more setup). Both go **inside a field**, never directly in a
template. Source: manual `math.md`.

## MathJax (preferred)

Supported out of the box on Anki 2.1+, AnkiMobile, AnkiDroid 2.9+.

- Inline: `\( \sqrt{x} \)`
- Display: `\[ \sum_{k=1}^{\infty} \frac{1}{k} \]`
- Content is **TeX format**. Use <kbd>Shift</kbd>+<kbd>Enter</kbd> for newlines
  inside an equation (a plain newline breaks MathJax).
- **mhchem** is built in for chemical equations.

Customize via a script in the card (load before content):

```html
<script>
MathJax.config.tex['macros'] = { R: '{\\mathbb {R}}' };
if (typeof is_already_run == 'undefined') {
  is_already_run = true
  MathJax.startup.getComponents();
}
</script>
```

> Do **not** change MathJax's standard delimiters — Anki has special cloze logic
> that depends on them.

## LaTeX

More capable but heavier: Anki calls LaTeX to render an image. Requires LaTeX
installed + **Generate LaTeX images** enabled in Preferences (off by default for
security — shared decks could run malicious commands). Images are generated on
desktop and synced; web/mobile can only *display* pre-generated images (bulk-generate
via **Tools → Check Media**).

- General form (inside a field):

  ```
  [latex]\begin{math}\sum_{k=1}^{\infty}\frac{1}{k}\end{math}[/latex]
  ```

- Shorthands:

  ```
  [$]...[/$]     ≡  [latex]\begin{math}...\end{math}[/latex]
  [$$]...[/$$]   ≡  [latex]\begin{displaymath}...\end{displaymath}[/latex]
  ```

- Custom packages: edit the note type's LaTeX **header/footer** (Options) to add
  `\usepackage{...}`.

## Template conflicts (older Anki)

In old versions, `{{`/`}}` in LaTeX could clash with field replacement. Modern
Anki (2.1.20+) no longer conflicts inside fields. For legacy support, put
`{{=<% %>=}}` at the **very top** of the front and back templates, then write
`<%field%>` instead of `{{field}}`.

## Cloze conflicts

Cloze is closed by `}}`, which collides with `}}` in LaTeX. Add a space before
any `}}` that is not a cloze close (math mode ignores the space):

```
{{c1::[$]\frac{foo}{\frac{bar}{baz} }[/$] blah.}}   ← works
{{c1::[$]\frac{foo}{\frac{bar}{baz}}[/$] blah.}}    ← breaks
```

For clozes where the space would change rendered text, insert an HTML comment
instead. See anki.cloze.

## Pitfalls

1. Put math/LaTeX **inside a field**, not the template.
2. MathJax needs <kbd>Shift</kbd>+<kbd>Enter</kbd> for newlines, not Enter.
3. Don't redefine MathJax delimiters — it breaks cloze handling.
4. LaTeX images only generate on desktop; run Check Media before syncing to
   mobile.
5. Enabling LaTeX image generation is a security risk with untrusted shared decks.
