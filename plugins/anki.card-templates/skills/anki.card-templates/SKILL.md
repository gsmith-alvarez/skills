---
name: anki.card-templates
description: Anki card template language — field replacement {{Field}}, conditionals {{#Field}}/{{^Field}}, special fields ({{Tags}}, {{FrontSide}}, {{Type}}, {{Deck}}, {{Subdeck}}, {{CardFlag}}, {{Card}}), filters (type:, cloze:, text:, hint:, tts:, furigana:/kana:/kanji:, cloze-only:), the {{FrontSide}} + <hr id=answer> divider, raw HTML/CSS, and card-generation rules. Use when writing or editing Anki card front/back templates or styling.
---

# Anki Card Templates

Templates are **HTML**; the Styling section is **CSS**. Edit them via the
**Cards…** button (Front template / Back template / Styling; <kbd>Ctrl</kbd>+<kbd>1/2/3</kbd>).
Source: manual `templates/fields.md`, `templates/generation.md`,
`templates/styling.md`, `templates/intro.md`.

## Basic field replacement

```
{{FieldName}}
```

- Case-sensitive: `{{Front}}` ≠ `{{front}}`.
- Arbitrary static text is allowed: `What's the capital of {{Country}}?`
- Default back template:

  ```
  {{FrontSide}}

  <hr id=answer>

  {{Back}}
  ```

  `{{FrontSide}}` repeats the front; `<hr id=answer>` is the **answer divider**
  (Anki auto-scrolls to it on Show Answer, esp. mobile). You may swap the `<hr>`
  for another element, but keep `id=answer` so the scroll anchor works.

## Newlines

Cards render like web pages: a literal newline collapses to a space. Use `<br>`
for line breaks — in templates **and** between two fields:

```
{{Field 1}}<br>
{{Field 2}}
```

## Special fields

| Template token | Meaning |
|---|---|
| `{{FrontSide}}` | Front template's rendered output (valid only in the back template) |
| `{{Tags}}` | Note's tags |
| `{{Type}}` | Note type name |
| `{{Deck}}` | Card's deck |
| `{{Subdeck}}` | Card's subdeck |
| `{{CardFlag}}` | Card's flag |
| `{{Card}}` | Card type label (e.g. "Forward") |

Case-sensitive (`{{Tags}}`, not `{{tags}}`). `{{FrontSide}}` won't replay front
audio on the back — re-include the audio field there if needed.

## Conditional replacement

```
{{#FieldName}} shown only if FieldName is non-empty {{/FieldName}}
{{^FieldName}} shown only if FieldName is empty      {{/FieldName}}
```

Real examples:

```
{{#Tags}}
    Tags: {{Tags}}
{{/Tags}}

{{#Notes}}<span style="color:blue;">{{/Notes}}
{{FieldToFormat}}
{{#Notes}}</span>{{/Notes}}
```

### Gating card generation (front only)

Because generation checks the **front** for blankness, wrap the whole front in a
conditional to require a field:

```
{{#Expression}}     ← no card if Expression empty
    {{Expression}}
    {{Notes}}
{{/Expression}}
```

Require **both** fields with nested conditionals. Putting the conditional on the
back only yields a blank-backed card. (See anki.note-types for the rule.)

## Filters (prefix a field name)

| Filter | Effect |
|---|---|
| `{{type:Field}}` | Type-in-the-answer box; compares your input to the field. **One per card**, single-line only. |
| `{{type:nc:Field}}` | Like `type:` but ignores diacritics/accents in the comparison. |
| `{{cloze:Field}}` | Renders cloze deletions — **cloze note type only** (see anki.cloze). |
| `{{text:Field}}` | Strips HTML formatting from the field (use for dictionary-link URLs). |
| `{{hint:Field}}` | Collapsible "show hint" link; hidden until clicked. |
| `{{tts en_US:Field}}` | Text-to-speech reads the field (Anki 2.1.20+; voices need OS/add-on). |
| `{{tts ja_JP voices=Apple_Otoya,Microsoft_Haruka:Field}}` | Choose voices; first available wins. `speed=0.8` optional; language required. |
| `{{tts en_US:cloze-only:Text}}` | Reads only the elided cloze sections (Anki 2.1.29+). |
| `{{furigana:Field}}` | Renders `Text[Ruby]` as `<ruby>` annotations (Japanese furigana). |
| `{{kana:Field}}` / `{{kanji:Field}}` | Show only the ruby text / only the base text. |

Multi-field/static TTS uses a block tag instead:

```
[anki:tts lang=en_US] This text is read. Here is {{Field1}} and {{Field2}}.[/anki:tts]
```

Type-answer boxes don't appear in the preview dialog or AnkiWeb. Style the
comparison via `code#typeans { … }` and colors `.typeGood`/`.typeBad`/`.typeMissed`.

## Right-to-left & ruby

```
<div dir="rtl">{{FieldWithRTL}}</div>
```

## HTML stripping caveat

Fields store HTML. For a dictionary link, `{{Expression}}` may contain
`<b>myword</b>`, breaking the URL. Use `{{text:Expression}}` to strip
formatting before substitution.

## Media in templates

- **Static media** (same on every card, e.g. a logo): name the file with a
  leading underscore (`_logo.jpg`) so it's bundled when sharing and ignored by
  Check Media, then reference it directly: `<img src="_logo.jpg">`.
- **Field references in media are NOT supported**: `<img src="{{Expression}}.jpg">`,
  `[sound:{{Word}}]`, and `[latex]{{Field}}[/latex]` may fail and won't be
  counted for unused-media/import/export. Put the media reference **inside the
  field** instead (see anki.media). Anki does not scan templates for media.

## Styling (CSS)

The Styling section is shared by all cards of the note type.

```css
.card {
  font-family: arial;
  font-size: 20px;
  text-align: center;
  color: black;
  background-color: white;
}
```

- **Card-specific CSS**: `.card1`, `.card2`, … target individual card types
  (e.g. color card 1 differently).
- **Field styling**: wrap a field in `<div class="mystyle1">…</div>` and define
  `.mystyle1 { … }` in Styling (key for non-Latin fonts).
- **Platform CSS**: `.win`, `.mac`, `.linux:not(.android)`, `.android` scope
  rules per platform.
- **Images**: Anki shrinks to fit by default; override with
  `img { max-width: 300px !important; max-height: 300px !important; }`
  (the `!important` matters on AnkiDroid).
- **Code**: `<code>…</code>` inline; `<pre><code>…</code></pre>` for blocks.
- **Audio replay buttons**: `.replay-button svg { width:20px; height:20px; }`.
- **Browser appearance**: a separate simplified template for the browser's
  Question/Answer columns (same syntax).

## Pitfalls

1. `{{field}}` is case-sensitive — typos create a "no such field" template error.
2. Conditionals must nest/close in order: `{{#A}}{{#B}}{{/B}}{{/A}}`. Mismatched
   closers (`{{/B}}` where `{{/A}}` expected) are template errors.
3. Generation looks only at the **front** — a blank front = no card, even if the
   back is full.
4. Never put media **references to fields** in a template; put them in fields.
5. `type:` answer comparison is single-line and one-per-card.
