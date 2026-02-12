# Lists & Named Ranges

## List

A complete list structure.

| Field | Type | Description |
|-------|------|-------------|
| `listProperties` | [`ListProperties`](#listproperties) | Formatting for all nesting levels. |
| `suggestedListPropertiesChanges` | map<string, `SuggestedListProperties`> | Suggested changes. |
| `suggestedInsertionId` | string | Suggestion ID if this list was suggested. |
| `suggestedDeletionIds[]` | string | Suggestion IDs proposing deletion. |

---

## ListProperties

Configuration for list formatting at each nesting level.

| Field | Type | Description |
|-------|------|-------------|
| `nestingLevels[]` | [`NestingLevel`](#nestinglevel) | Formatting for each depth (0 = top level). |

---

## NestingLevel

Formatting rules for a specific nesting depth.

| Field | Type | Description |
|-------|------|-------------|
| `bulletAlignment` | enum [`BulletAlignment`](./11-enums.md#bulletalignment) | Horizontal bullet positioning. |
| `format` | string | Printf-style format string for numbering. |
| `glyphFormat` | string | Character format for bullets (e.g. `%0.`, `%a.`). |
| `glyphSymbol` | string | The bullet character itself. |
| `glyphType` | enum [`GlyphType`](./11-enums.md#glyphtype) | Bullet symbol category. |
| `indentFirstLine` | [`Dimension`](./12-common-types.md#dimension) | First line indentation. |
| `indentStart` | [`Dimension`](./12-common-types.md#dimension) | Start margin indentation. |
| `startNumber` | integer | Starting value for numbered lists. |
| `textStyle` | [`TextStyle`](./05-styles.md#textstyle) | Styling applied to bullet text. |

### Sample Response — Multi-Level Bullet List

```json
{
  "listProperties": {
    "nestingLevels": [
      {
        "bulletAlignment": "START",
        "glyphSymbol": "●",
        "glyphFormat": "%0",
        "indentFirstLine": { "magnitude": 18, "unit": "PT" },
        "indentStart": { "magnitude": 36, "unit": "PT" },
        "textStyle": { "underline": false },
        "startNumber": 1
      },
      {
        "bulletAlignment": "START",
        "glyphSymbol": "○",
        "glyphFormat": "%1",
        "indentFirstLine": { "magnitude": 54, "unit": "PT" },
        "indentStart": { "magnitude": 72, "unit": "PT" },
        "textStyle": { "underline": false },
        "startNumber": 1
      },
      {
        "bulletAlignment": "START",
        "glyphSymbol": "■",
        "glyphFormat": "%2",
        "indentFirstLine": { "magnitude": 90, "unit": "PT" },
        "indentStart": { "magnitude": 108, "unit": "PT" },
        "textStyle": { "underline": false },
        "startNumber": 1
      }
    ]
  }
}
```

> A 3-level bullet list with different glyph symbols at each level: ● (filled circle) at level 0, ○ (hollow circle) at level 1, ■ (filled square) at level 2. Each level increases indentation by 36 PT (18→54→90 for first line, 36→72→108 for start). The `glyphFormat` uses `%N` where N is the nesting level index. Lists can define up to 9 nesting levels (0–8).

---

## Bullet

List formatting applied to a paragraph.

| Field | Type | Description |
|-------|------|-------------|
| `listId` | string | The ID of the list this paragraph belongs to. |
| `nestingLevel` | integer | Nesting depth (0 = top level). |
| `textStyle` | [`TextStyle`](./05-styles.md#textstyle) | Styling specific to the bullet. |

### Sample Response — Nested List Item

```json
{
  "startIndex": 8100,
  "endIndex": 8126,
  "paragraph": {
    "elements": [
      {
        "startIndex": 8100,
        "endIndex": 8126,
        "textRun": {
          "content": "Tie in notifications here\n",
          "textStyle": {}
        }
      }
    ],
    "paragraphStyle": {
      "namedStyleType": "NORMAL_TEXT",
      "direction": "LEFT_TO_RIGHT",
      "indentFirstLine": { "magnitude": 54, "unit": "PT" },
      "indentStart": { "magnitude": 72, "unit": "PT" }
    },
    "bullet": {
      "listId": "kix.m6yi3wvzwcl5",
      "nestingLevel": 1,
      "textStyle": {}
    }
  }
}
```

> A level-1 (sub-bullet) list item. The `nestingLevel: 1` determines which glyph and indentation from the list's `nestingLevels` array to use. The paragraph's `indentFirstLine` and `indentStart` match the list definition's level-1 values (54 PT and 72 PT respectively). The `listId` links this paragraph to its list definition in the tab's `lists` dictionary.

---

## NamedRanges

Container for named ranges sharing the same name.

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | The shared name. |
| `namedRanges[]` | [`NamedRange`](#namedrange) | Individual ranges with this name. |

---

## NamedRange

A labeled range within a document for programmatic reference.

| Field | Type | Description |
|-------|------|-------------|
| `namedRangeId` | string | Output only. Unique identifier. |
| `name` | string | The user-visible name (1–256 UTF-16 code units). |
| `ranges[]` | [`Range`](./12-common-types.md#range) | The content ranges. |
