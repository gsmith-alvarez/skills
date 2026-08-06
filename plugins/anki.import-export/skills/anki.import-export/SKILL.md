---
name: Anki Import & Export
description: Bulk-creating Anki notes/cards from text files (CSV/TSV) and packaged decks (.apkg/.colpkg) — field separators, quoting/escaping, HTML newlines, file headers (#separator, #html, #tags, #columns, #notetype, #deck, #notetype column, #deck column, #tags column, #guid column), duplicate/GUID handling, and export options. Use when generating cards in bulk or sharing decks.
---

# Anki Import & Export

Two bulk paths: **text files** (CSV/TSV, via File → Import) and **packaged
decks** (.apkg/.colpkg). Source: manual `importing/text-files.md`,
`importing/packaged-decks.md`, `exporting.md`.

## Text-file import

Any plain-text file with fields separated by comma / semicolon / tab, in
**UTF-8**, imports if:

- The first (non-comment) line sets the field count. Later rows with **fewer**
  fields → missing fields blank; **extra** fields → dropped.
- Anki auto-guesses the separator; override it (or force via headers) in the
  import dialog.
- Fields map to any note field, including a tags field, chosen at import time.

```
apple;banana;grape
first field;second field;third field
```

### Escaping newlines / separators

**Quote the field** (CSV rules; a `"` inside becomes `""`):

```
hello;"this is
a two line answer"
"this includes a ; (semicolon)";another field
field one;"field two with ""escaped quotes"" inside it"
```

**Or use HTML `<br>`** (needs **Allow HTML in fields** on import):

```
hello; this is<br>a two line answer
```

> Escaped multi-line fields break **cloze deletions that span lines** — use HTML
> newlines for those instead.

### Comments & tags

- Lines starting with `#` are ignored (unless they're a header, below).
- A `tags` column maps to the note's tags (space-separated).

### File headers (`#key:value`, Anki 2.1.54+)

Listed on separate lines at the top of the file:

| Header | Values | Effect |
|---|---|---|
| `separator` | `Comma`/`Semicolon`/`Tab`/`Space`/`Pipe`/`Colon` or the literal char | Force the field separator |
| `html` | `true`/`false` | Treat file as HTML |
| `tags` | space-separated list | Add these tags to every imported note |
| `columns` | names separated by the separator | Set column count + shown names |
| `notetype` | note type name or id | Preset the note type (if it exists) |
| `deck` | deck name or id | Preset the deck (if it exists) |
| `notetype column` | `1`,`2`,… | Which column holds each row's note type |
| `deck column` | `1`,`2`,… | Which column holds each row's deck |
| `tags column` | `1`,`2`,… | Which column holds each row's tags |
| `guid column` | `1`,`2`,… | Which column holds each row's GUID |

With a `notetype column`/`deck column`, the first **regular** column maps to the
first field, the second to the second field, and so on — letting one file mix
note types (e.g. `Basic` and `Cloze`).

```tsv
#separator:Tab
#html:true
#notetype column:1
#deck column:2
#tags:MyTag
#columns:Type	Deck	Field1	Field2
Basic	MyDeck::Topic	Question	Answer
Cloze	MyDeck::Topic	{{c1::Text}}	Extra
```

> **Fallback Strategy:** When generating import files programmatically, also consider providing separate TSV files per note type (e.g. `Basic_Cards.tsv` with `#notetype:Basic` and `Cloze_Cards.tsv` with `#notetype:Cloze`). This avoids manual column mapping errors if the user's Anki version does not parse multi-note-type headers automatically.

### Duplicates & updating

- Anki keys duplicates on the **first field within the note type**. Default: an
  existing same-type note with a matching first field is **updated** from the
  file; you can switch to ignore duplicates or import as new.
- **Match scope**: `note type` (default) or `note type and deck`.
- **GUID column**: if provided and non-empty, Anki uses it for duplicate checks
  and will **not** create a duplicate for an existing GUID. For your own IDs,
  prefer putting them in the first field rather than Anki's internal GUID.

## Exporting

- **Notes in Plain Text**: tab-separated; HTML formatting embedded. If you keep
  the first field unchanged, re-importing updates the notes (same note type).
- **Packaged decks** bundle notes, note types, and media into one file.

### `.apkg` (deck package)

Exports a single deck (+ child decks). On import it is **added** to your
collection (not replaced); notes already present are updated to the **most
recent modification time**. Export options: Include Scheduling Information,
Include Deck Presets, Include Media, Support older Anki versions. When importing
a *shared* deck, leave "Import any learning progress" off so you don't inherit
the author's intervals/leech tags (use Set Due Date to reset if needed).

### `.colpkg` (collection package)

Exports your **entire collection** (all decks + scheduling). On import it
**replaces** your current collection. Use for backup/device transfer. Existing
media is not deleted.

## Pitfalls

1. Files must be **plain text + UTF-8** (save spreadsheets as CSV via LibreOffice
   for reliable UTF-8 + multi-line).
2. Map fields, including a tags column, in the import dialog.
3. Cloze spanning lines → use HTML `<br>`, not quoted multi-line.
4. Media references (`[sound:]`, `<img>`) go in fields and need **Allow HTML**.
5. `.apkg` merges by modification time; `.colpkg` overwrites the whole collection.
6. **Code String Escaping (LaTeX `\to` in TSV generators):** When writing TSV strings in programming languages like Python, unescaped TeX commands like `\to` evaluate to `\t` (a literal TAB character) + `o`. This injects unexpected column breaks mid-field, corrupting TSV formatting and causing Anki to fail or collapse all rows into a single row. Always use raw strings (`r"..."`) or double-escape backslashes (`\\to`).
