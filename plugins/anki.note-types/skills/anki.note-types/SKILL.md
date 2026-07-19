---
name: Anki Note Types
description: Anki's data model — notes vs cards, fields, note types, and the built-in types (Basic, Basic (and reversed), Basic (optional reversed), Basic (type in the answer), Cloze, Image Occlusion). Covers card-generation rules, deck override, and tags. Use when designing note types or deciding how cards are generated from notes.
---

# Anki Note Types

Anki stores **notes**, then generates **cards** from them. Understanding this
split is the foundation of card generation: you author notes (structured
fields), and Anki's per-note-type **card types** (templates) decide which cards
get created. Source: manual `getting-started.md` (Key Concepts), `editing.md`,
`templates/generation.md`.

## The model

```
collection
 └─ decks                (broad study categories; double-colon tree "A::B")
     └─ notes            (one entry of related info, split into fields)
         ├─ fields        (Front, Back, Expression, … — typed pieces of info)
         └─ card types    (blueprints: a front template + a back template)
             └─ cards      (one card created per card type per note)
```

- A **note** holds related info in separate **fields** (e.g. `French`,
  `English`, `Page`). Splitting into fields — not one blob — lets you sort,
  move content between front/back, and filter per field later.
- A **card type** (a.k.a. template) is the blueprint naming which fields appear
  on the front and back. Anki creates **one card per card type** for each note.
- Editing a note updates **all** its cards at once; fixing a typo fixes every
  card that uses the field.

## Note types

Each note type has its own set of fields + card types. Create one per broad
topic (e.g. `French`, `Capital Cities`, `Anatomy`), not per lesson. Manage via
**Tools → Manage Note Types**. "Add" bases it on a built-in type; "Clone" bases
it on one already in your collection.

Notes and note types are **collection-wide**, not per-deck: you can mix note
types in one deck, and route a note's cards to different decks via deck
override (below).

### Built-in note types

| Note type | Fields | Cards generated |
|---|---|---|
| **Basic** | `Front`, `Back` | 1 (Front→Back) |
| **Basic (and reversed card)** | `Front`, `Back` | 2 (Front→Back **and** Back→Front) |
| **Basic (optional reversed card)** | `Front`, `Back`, `Add Reverse` | 1 forward; +1 reversed **only if `Add Reverse` is non-empty** (its content is never shown) |
| **Basic (type in the answer)** | `Front`, `Back` | 1, with a type-answer box on the front (see `type:` filter in anki.card-templates) |
| **Cloze** | `Text`, `Extra` | one per cloze number — see anki.cloze |
| **Image Occlusion** | image + `Header`, `Back Extra`, `Comments` | one per shape/group — see anki.cloze |

For language study, prefer two cards (recognition + production) via the reversed
types rather than reversing a single card — Anki then schedules each direction
independently.

## Customizing fields

Add / rename / reposition fields via the **Fields…** button. Properties:

- **Editing font** — font/size while editing (does not affect review).
- **Sort field** — shows this field in the browser's Sort Field column (one only).
- **Reverse text direction** — RTL editing aid (review display still needs template CSS).
- **Use HTML editor by default**, **Collapse by default**.
- **Exclude from unqualified searches** — hide this field from bare searches.

> **Reserved field names** — never name a field `Tags`, `Type`, `Deck`, `Card`,
> or `FrontSide`: they collide with [special fields](templates/fields.md) and
> misbehave.

## Duplicate check

Anki checks the **first field** for uniqueness **within the note type**. Two
notes with the same first-field value in the same type warn as duplicates. Use a
distinct note type per language/topic so cross-topic duplicates don't clash.

## Deck override & tags

- **Deck override** (per card type, via the template Options button) routes that
  card type's cards into a specific deck, ignoring the Add-window deck. Useful to
  split production vs recognition cards into separate decks.
- **Tags** live at the **note** level (every sibling card shares them). For
  per-card marking, use **flags** instead (flags are per-card). A tag named
  `marked` is treated specially (star in review/browser).

## Card generation rules

Anki **will not create a card whose front side is blank**. Implications:

- If a front template contains only `{{EmptyField}}`, no card is made.
- Non-field text does **not** count toward generation. `Where is {{Country}}?`
  yields **no card** if `Country` is empty.
- If you later edit a note so a previously-blank field becomes non-empty, the
  card is auto-created. If edits blank a card's front, the card is **not**
  deleted immediately (data-loss guard) — remove it via **Tools → Empty Cards**.
- You cannot manually delete an individual card: editing the note would recreate
  it. Instead empty the relevant conditional field, then run Empty Cards.
- Adding a new note that produces no cards still creates a blank card from the
  first template, so you can fill it in later.

### Selective generation

To generate an extra card for only some notes, add a marker field (e.g. `Extra`
containing `1`) and gate the card's front on it:

```
{{#Extra}}        ← card only generated when Extra is non-empty
    {{Expression}}
{{/Extra}}
```

Wrap the **entire front** in the conditional; doing it on the back only produces
a blank-backed card. See anki.card-templates for conditional syntax.

## Pitfalls

1. Don't cram audio/picture/hint/translation into one `Front` blob "because it's
   one card" — you lose sorting, per-field front/back moves, and filtering.
   Split into fields.
2. Reversed-via-single-card hides the back's extra info and merges scheduling of
   both directions — use a real reversed note type.
3. `Add Reverse` content is never shown; it's purely a switch.
4. Cloze and Image Occlusion are special note types — you **clone** them to
   customize; you cannot add card templates to the cloze type.
