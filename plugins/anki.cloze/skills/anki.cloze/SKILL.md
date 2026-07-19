---
name: Anki Cloze Deletion
description: Cloze deletion syntax and generation — {{c1::text}}, {{c1::text::hint}}, multiple clozes → multiple cards, numbering rules, nested clozes, the cloze note type (single card template using {{cloze:Text}}), per-card conditionals {{#c1}}, type:cloze, cloze+LaTeX delimiter conflicts, and Image Occlusion. Use when generating cloze cards.
---

# Anki Cloze Deletion

Cloze = hiding one or more words in a sentence. The **Cloze** note type is
special: it has a single card type and generates **one card per cloze number**.
Source: manual `editing.md` (Cloze Deletion, Image Occlusion),
`templates/generation.md` (Cloze Templates), `templates/errors.md`.

## Syntax

Inside the `Text` field:

```
Canberra was founded in {{c1::1913}}.
```

- `{{c1::…}}` marks one deletion. On review the question shows `Canberra was
  founded in […].`; the answer reveals the full sentence.
- **Each distinct number → one card.** With two numbers:

  ```
  {{c2::Canberra}} was founded in {{c1::1913}}.
  ```

  Anki makes **2 cards**: one asks `… was founded in 1913`, the other asks
  `Canberra was founded in …`.

- **Same number, multiple sections → one card** with all hidden. Hold
  <kbd>Alt</kbd> (<kbd>Option</kbd> on Mac) while clozing to reuse the same number
  instead of incrementing.
- **Hints** that don't match the text:

  ```
  {{c1::Canberra::city}}   →   [city] was founded in 1913.
  ```

- Deletions need **not** fall on word boundaries (`anberra` gives a partial hint:
  `C[…] was founded in 1913`).

## Nested clozes (Anki 2.1.56+)

```
{{c1::Canberra was {{c2::founded}}}} in 1913
```

- The inner cloze is entirely inside the outer one. **No partial overlap** is
  supported (e.g. two deletions sharing the word "was").
- Nesting limit: 3 levels in Anki 24.11, ~8 in other versions (slower as you
  approach it; not extensible). Keep nesting shallow.

## The cloze note type

- Fields: `Text` (holds the `{{cN::…}}` markup) and `Extra` (shown on the answer
  side of every cloze card).
- **Single card type.** Clone it to customize formatting; you cannot add extra
  card templates to it.
- Templates **must** contain a cloze filter on both front and back:

  ```
  {{cloze:Text}}
  {{cloze:Text}}
  {{type:cloze:Text}}   ← optional, on both sides for type-answer
  {{Extra}}
  ```

  If the template loses its `{{cloze:Text}}` filter, **all** cloze cards go
  blank — restore `{{cloze:Text}}` to fix.

## Per-card conditionals

Reference which cloze card is rendering with `{{#c1}}`…`{{/c1}}`,
`{{#c2}}`…`{{/c2}}`, etc. (these are special cloze conditionals, not field
names):

```
{{cloze:Text}}

{{#c1}}
    {{Hint1}}
{{/c1}}

{{#c2}}
    {{Hint2}}
{{/c2}}
```

## Type-in-the-answer for cloze

Add `{{type:cloze:Text}}` to **both** front and back; if several sections are
elided, separate your typed answers with a comma.

## Generation & cleanup

- Editing text so a cloze number is removed/renumbered can blank an already-made
  card (e.g. card 3 vanishes if `c3` becomes `c1`). Clean these up with
  **Tools → Empty Cards**.
- Because each number is its own card, a sentence with three separate numbers
  makes three cards:

  ```
  {{c1::This}} is a {{c2::sample}} {{c3::sentence}}.
  ```

## Cloze + LaTeX conflict

Cloze deletions are terminated by `}}`, which collides with `}}` inside LaTeX.
Fix by inserting a space before any `}}` that is **not** a cloze close (LaTeX
ignores math-mode spaces):

```
{{c1::[$]\frac{foo}{\frac{bar}{baz} }[/$] blah blah.}}   ← works
{{c1::[$]\frac{foo}{\frac{bar}{baz}}[/$] blah blah.}}    ← breaks
```

For programming-language clozes where the space would alter rendered text, use an
HTML comment instead. (See anki.math for the `{{=<% %>=}}` template-conflict
workaround too.)

## Image Occlusion (Anki 23.10+)

A cloze variant on **images**. Pick the `Image Occlusion` note type, load an
image, then add shapes (Rectangle / Ellipse / Polygon). Modes:

- **Hide All, Guess One** — all areas hidden, one revealed at a time.
- **Hide One, Guess One** — only one area hidden per step.

Fields: `Header` (above image, both sides), `Back Extra` (below image, back),
`Comments` (not shown). Anki creates **one card per shape or grouped shape**
(grouped shapes → one card).

## Pitfalls

1. `{{cloze:Field}}` only works on the **cloze note type** — on a regular type it
   won't generate correctly.
2. Each number = one card; renumbering/removing numbers blanks old cards.
3. `}}` inside LaTeX breaks cloze closing — add the spacing or HTML-comment fix.
4. Cloze note type can't gain extra card templates; clone to restyle.
