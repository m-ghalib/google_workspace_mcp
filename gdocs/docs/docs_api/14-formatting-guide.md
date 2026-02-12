# Formatting Guide — Practical API Patterns

How the Google Docs API actually works in practice, derived from real API responses.

> All JSON examples are from a real document fetched with `includeTabsContent=true`.

---

## 1. Document Structure — The Index Model

A Google Doc is a flat array of `StructuralElement` objects, each tagged with `startIndex` / `endIndex`. Understanding this index model is the foundation for every write operation.

### Real document index map

```
Index       Element
──────────  ──────────────────────────────────────────────
   N/A-  1  SectionBreak (CONTINUOUS) — always first, never modify
     1-  2  Paragraph "\n" [NORMAL_TEXT]
     2- 48  Paragraph "Partner Management Roles..." [TITLE, CENTER]
    48- 64  Paragraph "Date Updated: ..." [NORMAL_TEXT]
    64- 76  Paragraph "Status: WIP\n" [NORMAL_TEXT]
    76- 90  Paragraph "Authors: ..." [NORMAL_TEXT]
    90-103  Paragraph "Consulted: ?\n" [NORMAL_TEXT]
   103-138  Paragraph "Purpose & How to Use This Document\n" [HEADING_1]
   138-139  Paragraph "\n" [HEADING_3]
   139-168  Paragraph "1.1 Why This Document Exists\n" [HEADING_2]
   168-250  Paragraph "This document addresses critical..." [NORMAL_TEXT]
       ...
   561-591  Paragraph "1.2 Who Should Reference This\n" [HEADING_2]
   591-1400 Table (7×3) — spans 809 indices
  1400-1401 Paragraph "\n" [HEADING_3]
```

### Index rules

1. **Sequential, non-overlapping.** One element's `endIndex` equals the next element's `startIndex`. No gaps, no overlaps.
2. **Index 0 is reserved.** Every tab starts with a `SectionBreak` at index 0-1. It's the only element with no `startIndex` field. Don't modify it.
3. **Newlines count.** Every paragraph ends with `\n` which occupies 1 index. The text `"Hello\n"` spans 6 indices.
4. **Exclusive end.** `endIndex` is exclusive. A paragraph at `[103-138]` has content at positions 103 through 137.
5. **UTF-16 code units.** Indices count UTF-16 code units, not characters. Most text = 1 unit per char. Emoji and some symbols = 2 units.

### Table nesting — +1 offset per level

Tables add a boundary character at each nesting level:

```
 591-1400  Table (7×3)
   592      └─ TableRow 0        (+1 from table start)
   593        └─ TableCell 0     (+1 from row start)
   594          └─ Paragraph     (+1 from cell start)
   594            └─ TextRun "Audience\n"  (matches paragraph)

   603        └─ TableCell 1     (== previous cell endIndex)
   604          └─ Paragraph     (+1 from cell start)
   604            └─ TextRun "Primary Sections\n"

   621        └─ TableCell 2
   622          └─ Paragraph
   622            └─ TextRun "Use Case\n"
   631      └─ TableRow 1        (== Row 0 endIndex)
   632        └─ TableCell 0
   633          └─ Paragraph
   633            └─ TextRun "Partner Management\n"
```

The +1 offsets are invisible boundary characters consumed by the table structure. To insert text into a table cell, target the cell's paragraph `startIndex`, not the cell's `startIndex`.

---

## 2. Paragraph Editing

### Insert text

Uses a `Location` (single index point). All content after the insertion point shifts right.

```json
{
  "insertText": {
    "location": { "index": 168 },
    "text": "New paragraph content.\n"
  }
}
```

To append to the end of the document body:

```json
{
  "insertText": {
    "endOfSegmentLocation": { "segmentId": "" },
    "text": "Appended text.\n"
  }
}
```

### Delete text

Uses a `Range` (startIndex + exclusive endIndex). Content after the deletion shifts left.

```json
{
  "deleteContentRange": {
    "range": { "startIndex": 168, "endIndex": 250 }
  }
}
```

### Replace text (at a known range)

Two operations in one batch: delete first, then insert at the same index.

```json
{
  "requests": [
    { "deleteContentRange": { "range": { "startIndex": 168, "endIndex": 250 } } },
    { "insertText": { "location": { "index": 168 }, "text": "Replacement text.\n" } }
  ]
}
```

Order matters — delete executes first, collapsing the range, then insert places new content at the same start position.

### Global find and replace

The only text operation that doesn't require indices:

```json
{
  "replaceAllText": {
    "containsText": { "text": "WIP", "matchCase": true },
    "replaceText": "FINAL"
  }
}
```

Returns `{ "occurrencesChanged": 3 }` in the response.

### Multi-operation batching

Operations in a `batchUpdate` execute **sequentially**. Each operation sees the document as modified by the previous one. This means indices shift.

**Process from highest index to lowest** to avoid shift conflicts:

```json
{
  "requests": [
    { "deleteContentRange": { "range": { "startIndex": 400, "endIndex": 450 } } },
    { "deleteContentRange": { "range": { "startIndex": 168, "endIndex": 250 } } }
  ]
}
```

If you process lowest-first, the first deletion shifts the second range's indices.

---

## 3. Named Styles — The Inheritance Model

### The 9 named styles

| Style | Font Size | Bold | keepLinesTogether | keepWithNext |
|-------|-----------|------|-------------------|--------------|
| NORMAL_TEXT | 11pt | false | false | false |
| TITLE | 26pt | — | true | true |
| SUBTITLE | 15pt (Arial) | — | true | true |
| HEADING_1 | 20pt | true | true | true |
| HEADING_2 | 16pt | true | true | true |
| HEADING_3 | 14pt | false | true | true |
| HEADING_4 | 12pt | — | true | true |
| HEADING_5 | 11pt | — | true | true |
| HEADING_6 | 11pt | — | true | true |

### How inheritance works

A named style definition specifies **all** default fields. An actual paragraph using that style only carries **overridden** fields. Compare:

**Named style definition** (in `namedStyles.styles[]`):
```json
{
  "namedStyleType": "HEADING_1",
  "textStyle": {
    "bold": true,
    "fontSize": { "magnitude": 20, "unit": "PT" }
  },
  "paragraphStyle": {
    "namedStyleType": "HEADING_1",
    "direction": "LEFT_TO_RIGHT",
    "keepLinesTogether": true,
    "keepWithNext": true
  }
}
```

**Actual paragraph using HEADING_1** (in `body.content[]`):
```json
{
  "startIndex": 103,
  "endIndex": 138,
  "paragraph": {
    "elements": [
      {
        "startIndex": 103,
        "endIndex": 138,
        "textRun": {
          "content": "Purpose & How to Use This Document\n",
          "textStyle": {
            "foregroundColor": {
              "color": { "rgbColor": { "red": 0.011, "green": 0.101, "blue": 0.427 } }
            },
            "fontSize": { "magnitude": 20, "unit": "PT" },
            "weightedFontFamily": { "fontFamily": "Poppins", "weight": 400 }
          }
        }
      }
    ],
    "paragraphStyle": {
      "headingId": "h.i9dx5sbhk9zn",
      "namedStyleType": "HEADING_1",
      "direction": "LEFT_TO_RIGHT",
      "spaceAbove": { "magnitude": 12, "unit": "PT" },
      "spaceBelow": { "magnitude": 6, "unit": "PT" }
    }
  }
}
```

What this reveals:
- The **definition** has `bold: true` — the **paragraph** doesn't repeat it (inherited)
- The **paragraph** adds `foregroundColor`, `weightedFontFamily`, `spaceAbove`, `spaceBelow` — these are overrides not in the definition
- `headingId` is auto-generated and unique per heading instance
- `textStyle: {}` (empty) on a text run means "inherit everything from the named style"

### Applying a named style via batchUpdate

```json
{
  "updateParagraphStyle": {
    "range": { "startIndex": 168, "endIndex": 250 },
    "paragraphStyle": { "namedStyleType": "HEADING_1" },
    "fields": "namedStyleType"
  }
}
```

The `fields` mask is **mandatory**. Without `"namedStyleType"` in `fields`, the update silently does nothing.

---

## 4. Text Styling — Character-Level Formatting

### The updateTextStyle request

```json
{
  "updateTextStyle": {
    "range": { "startIndex": 594, "endIndex": 603 },
    "textStyle": {
      "bold": true,
      "foregroundColor": {
        "color": { "rgbColor": { "red": 1, "green": 1, "blue": 1 } }
      }
    },
    "fields": "bold,foregroundColor"
  }
}
```

This makes "Audience" bold white text. The `fields` mask lists exactly which properties to update — unlisted properties are left unchanged.

### Available TextStyle properties

| Property | Type | Example |
|----------|------|---------|
| `bold` | boolean | `true` |
| `italic` | boolean | `true` |
| `underline` | boolean | `true` |
| `strikethrough` | boolean | `true` |
| `smallCaps` | boolean | `true` |
| `fontSize` | Dimension | `{ "magnitude": 20, "unit": "PT" }` |
| `weightedFontFamily` | object | `{ "fontFamily": "Poppins", "weight": 400 }` |
| `foregroundColor` | OptionalColor | `{ "color": { "rgbColor": { "red": 0.0, "green": 0.0, "blue": 0.0 } } }` |
| `backgroundColor` | OptionalColor | Same structure as foregroundColor |
| `baselineOffset` | enum | `"SUPERSCRIPT"`, `"SUBSCRIPT"`, `"NONE"` |
| `link` | Link | `{ "url": "https://example.com" }` |

### The color model — 3 layers deep

```
OptionalColor → Color → RgbColor
```

```json
{
  "foregroundColor": {
    "color": {
      "rgbColor": { "red": 0.054, "green": 0.415, "blue": 0.929 }
    }
  }
}
```

Values are 0.0–1.0 floats. White = `{ "red": 1, "green": 1, "blue": 1 }`. Black = all zeros (or omit the color entirely).

### Empty `{}` vs omitted — different meanings

| Pattern | Meaning | Example |
|---------|---------|---------|
| `"textStyle": {}` | Inherit all properties from named style | Title paragraph's text run |
| `"backgroundColor": {}` | Explicitly transparent / no color | Most text backgrounds |
| Field omitted entirely | Inherit from parent context | `bold` omitted = inherits from named style |
| `{ "unit": "PT" }` (no magnitude) | Zero value (0pt) | Zero-width borders, zero padding |

---

## 5. Lists — Bullets and Numbered

### Creating a list

```json
{
  "createParagraphBullets": {
    "range": { "startIndex": 250, "endIndex": 560 },
    "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
  }
}
```

The range must cover **complete paragraphs** including their trailing `\n` characters.

### Bullet presets

| Preset | Visual |
|--------|--------|
| `BULLET_DISC_CIRCLE_SQUARE` | ● ○ ■ (default bullets) |
| `BULLET_CHECKBOX` | ☐ checkboxes |
| `BULLET_STAR_CIRCLE_SQUARE` | ★ ● ■ |
| `BULLET_ARROW_DIAMOND_DISC` | → ◆ ● |
| `BULLET_DIAMONDX_ARROW3D_SQUARE` | ◇ ➤ ■ |
| `BULLET_ARROW3D_CIRCLE_SQUARE` | ➤ ● ■ |
| `BULLET_LEFTTRIANGLE_DIAMOND_DISC` | ◁ ◆ ● |
| `NUMBERED_DECIMAL_ALPHA_ROMAN` | 1. a. i. |
| `NUMBERED_DECIMAL_ALPHA_ROMAN_PARENS` | 1) a) i) |
| `NUMBERED_DECIMAL_NESTED` | 1. 1.1. 1.1.1. |
| `NUMBERED_UPPERALPHA_ALPHA_ROMAN` | A. a. i. |
| `NUMBERED_UPPERROMAN_UPPERALPHA_DECIMAL` | I. A. 1. |
| `NUMBERED_ZERODECIMAL_ALPHA_ROMAN` | 01. a. i. |

### What happens in the document structure

When you apply bullets, the API creates:

1. A `List` entry in `document.lists` map (or `documentTab.lists`):
```json
{
  "kix.abc123def456": {
    "listProperties": {
      "nestingLevels": [
        { "bulletAlignment": "START", "glyphType": "GLYPH_TYPE_UNSPECIFIED", "indentFirstLine": { "magnitude": 18, "unit": "PT" }, "indentStart": { "magnitude": 36, "unit": "PT" } },
        { "bulletAlignment": "START", "glyphType": "GLYPH_TYPE_UNSPECIFIED", "indentFirstLine": { "magnitude": 54, "unit": "PT" }, "indentStart": { "magnitude": 72, "unit": "PT" } }
      ]
    }
  }
}
```

2. Each paragraph in the range gets a `bullet` field:
```json
{
  "paragraph": {
    "bullet": {
      "listId": "kix.abc123def456",
      "nestingLevel": 0
    },
    "elements": [ "..." ],
    "paragraphStyle": { "namedStyleType": "NORMAL_TEXT" }
  }
}
```

### Removing list formatting

```json
{
  "deleteParagraphBullets": {
    "range": { "startIndex": 250, "endIndex": 560 }
  }
}
```

Preserves all text content — only removes the bullet/number formatting.

### Controlling nesting level

Adjust `indentStart` on the paragraph to change list nesting depth:

```json
{
  "updateParagraphStyle": {
    "range": { "startIndex": 344, "endIndex": 415 },
    "paragraphStyle": { "indentStart": { "magnitude": 72, "unit": "PT" } },
    "fields": "indentStart"
  }
}
```

---

## 6. Table Operations

### Reading table structure (from API response)

A table is a deeply nested hierarchy:

```json
{
  "startIndex": 591,
  "endIndex": 1400,
  "table": {
    "rows": 7,
    "columns": 3,
    "tableRows": [
      {
        "startIndex": 592,
        "endIndex": 631,
        "tableCells": [
          {
            "startIndex": 593,
            "endIndex": 603,
            "content": [
              {
                "startIndex": 594,
                "endIndex": 603,
                "paragraph": {
                  "elements": [
                    {
                      "startIndex": 594,
                      "endIndex": 603,
                      "textRun": {
                        "content": "Audience\n",
                        "textStyle": { "bold": true, "foregroundColor": { "color": { "rgbColor": { "red": 1, "green": 1, "blue": 1 } } } }
                      }
                    }
                  ]
                }
              }
            ],
            "tableCellStyle": {
              "rowSpan": 1,
              "columnSpan": 1,
              "backgroundColor": { "color": { "rgbColor": { "red": 0.054, "green": 0.415, "blue": 0.929 } } },
              "paddingLeft": { "magnitude": 5, "unit": "PT" },
              "paddingRight": { "magnitude": 5, "unit": "PT" },
              "paddingTop": { "magnitude": 5, "unit": "PT" },
              "paddingBottom": { "magnitude": 5, "unit": "PT" },
              "contentAlignment": "TOP"
            }
          }
        ],
        "tableRowStyle": { "minRowHeight": { "unit": "PT" } }
      }
    ]
  }
}
```

### Creating a table

```json
{
  "insertTable": {
    "location": { "index": 1400 },
    "rows": 3,
    "columns": 4
  }
}
```

Creates an empty table — each cell contains a single empty paragraph. To populate cells, you must `insertText` into each cell's paragraph index.

### Inserting text into a cell

After creating or finding a table, read the document to discover each cell's paragraph `startIndex`, then:

```json
{
  "insertText": {
    "location": { "index": 594 },
    "text": "Cell content"
  }
}
```

**Index refreshing is critical.** After inserting into one cell, all subsequent cell indices shift. Re-read the document before each cell insertion.

### Adding/removing rows and columns

Uses `TableCellLocation` — a reference cell that identifies the row or column:

```json
{
  "insertTableRow": {
    "tableCellLocation": {
      "tableStartLocation": { "index": 591 },
      "rowIndex": 2,
      "columnIndex": 0
    },
    "insertBelow": true
  }
}
```

```json
{
  "insertTableColumn": {
    "tableCellLocation": {
      "tableStartLocation": { "index": 591 },
      "rowIndex": 0,
      "columnIndex": 1
    },
    "insertRight": true
  }
}
```

Delete variants use the same `TableCellLocation` pattern — the entire row/column containing the referenced cell is removed.

### Styling cells

```json
{
  "updateTableCellStyle": {
    "tableRange": {
      "tableCellLocation": {
        "tableStartLocation": { "index": 591 },
        "rowIndex": 0,
        "columnIndex": 0
      },
      "rowSpan": 1,
      "columnSpan": 3
    },
    "tableCellStyle": {
      "backgroundColor": { "color": { "rgbColor": { "red": 0.054, "green": 0.415, "blue": 0.929 } } },
      "paddingTop": { "magnitude": 5, "unit": "PT" },
      "paddingBottom": { "magnitude": 5, "unit": "PT" },
      "paddingLeft": { "magnitude": 5, "unit": "PT" },
      "paddingRight": { "magnitude": 5, "unit": "PT" },
      "contentAlignment": "TOP"
    },
    "fields": "backgroundColor,paddingTop,paddingBottom,paddingLeft,paddingRight,contentAlignment"
  }
}
```

### Column widths and row heights

```json
{
  "updateTableColumnProperties": {
    "tableStartLocation": { "index": 591 },
    "columnIndices": [0, 1, 2],
    "tableColumnProperties": {
      "widthType": "FIXED_WIDTH",
      "width": { "magnitude": 200, "unit": "PT" }
    },
    "fields": "widthType,width"
  }
}
```

```json
{
  "updateTableRowStyle": {
    "tableStartLocation": { "index": 591 },
    "rowIndices": [0],
    "tableRowStyle": { "tableHeader": true },
    "fields": "tableHeader"
  }
}
```

### Merge and unmerge cells

```json
{
  "mergeTableCells": {
    "tableRange": {
      "tableCellLocation": {
        "tableStartLocation": { "index": 591 },
        "rowIndex": 0,
        "columnIndex": 0
      },
      "rowSpan": 1,
      "columnSpan": 3
    }
  }
}
```

### Pin header rows

```json
{
  "pinTableHeaderRows": {
    "tableStartLocation": { "index": 591 },
    "pinnedHeaderRowsCount": 1
  }
}
```

---

## 7. Gotchas Quick Reference

| Gotcha | What happens | Fix |
|--------|-------------|-----|
| Missing `fields` mask on `Update*` request | Update silently does nothing | Always specify the field mask |
| Modifying index 0 | API error (it's the sectionBreak) | Content operations start at index 1 |
| Forward-order multi-insert | Indices shift, later inserts land in wrong positions | Process highest index to lowest |
| Paragraph text missing `\n` | Paragraph boundary corruption | Always end inserted paragraph text with `\n` |
| `{}` vs field omission | `{}` = explicit unset/transparent; omitted = inherit from parent | Choose intentionally based on intent |
| `{ "unit": "PT" }` no magnitude | Zero value (0pt), not "use default" | Always include magnitude for non-zero values |
| Table cell insertion without re-reading doc | Stale indices → wrong-cell writes | Re-read document after each cell insertion |
| `endIndex` is exclusive | Range `[10, 11]` covers 1 character at position 10 | `endIndex = lastPosition + 1` |
| UTF-16 code units | Emoji counts as 2 index positions | Use Python's `len(text.encode('utf-16-le')) // 2` for index math |
| Tab targeting | Operations default to first tab only | Include `tabId` in Range/Location for multi-tab documents |
| Only 7 of 37 requests return data | Most `replies[]` entries are `{}` | Check docs for which requests produce meaningful responses |
