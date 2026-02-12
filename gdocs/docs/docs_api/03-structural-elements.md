# Structural Elements

Block-level elements that compose the document body.

## Body

The main content container of a document or tab.

| Field | Type | Description |
|-------|------|-------------|
| `content[]` | [`StructuralElement`](#structuralelement) | The structural elements composing the body. |

### Sample Response

```json
{
  "content": [
    {
      "endIndex": 1,
      "sectionBreak": {
        "sectionStyle": { "columnSeparatorStyle": "NONE", "contentDirection": "LEFT_TO_RIGHT", "sectionType": "CONTINUOUS" }
      }
    },
    {
      "startIndex": 2,
      "endIndex": 48,
      "paragraph": {
        "elements": [ "..." ],
        "paragraphStyle": { "namedStyleType": "TITLE", "alignment": "CENTER" }
      }
    },
    {
      "startIndex": 593,
      "endIndex": 1234,
      "table": { "rows": 7, "columns": 3, "tableRows": [ "..." ] }
    }
  ]
}
```

> The first element is always a `sectionBreak` at index 0. Subsequent elements are `paragraph` or `table` entries. This sample document contains 273 structural elements across 247 paragraphs and 25 tables.

---

## StructuralElement

A block-level element. Exactly one of the union fields will be set.

| Field | Type | Description |
|-------|------|-------------|
| `startIndex` | integer | Zero-based start position in UTF-16 code units. |
| `endIndex` | integer | Zero-based end position (exclusive). |

### Union field (one of):

| Field | Type | Description |
|-------|------|-------------|
| `paragraph` | [`Paragraph`](#paragraph) | A paragraph element. |
| `sectionBreak` | [`SectionBreak`](#sectionbreak) | A section break. |
| `table` | [`Table`](#table) | A table element. |
| `tableOfContents` | [`TableOfContents`](#tableofcontents) | A table of contents. |

---

## Paragraph

A block of text with consistent styling.

| Field | Type | Description |
|-------|------|-------------|
| `elements[]` | [`ParagraphElement`](./04-paragraph-elements.md) | Inline content within the paragraph. |
| `paragraphStyle` | [`ParagraphStyle`](./05-styles.md#paragraphstyle) | Paragraph-level formatting. |
| `suggestedParagraphStyleChanges` | map<string, `SuggestedParagraphStyle`> | Suggested paragraph style changes keyed by suggestion ID. |
| `bullet` | [`Bullet`](./07-lists-named-ranges.md#bullet) | List formatting if this paragraph is a list item. |
| `suggestedBulletChanges` | map<string, `SuggestedBullet`> | Suggested bullet changes. |
| `positionedObjectIds[]` | string | IDs of positioned objects anchored to this paragraph. |

### Sample Response

```json
{
  "startIndex": 2,
  "endIndex": 48,
  "paragraph": {
    "elements": [
      {
        "startIndex": 2,
        "endIndex": 48,
        "textRun": {
          "content": "Partner Management Roles and Responsibilities\n",
          "textStyle": {}
        }
      }
    ],
    "paragraphStyle": {
      "headingId": "h.c2wvo57xe3r0",
      "namedStyleType": "TITLE",
      "alignment": "CENTER",
      "direction": "LEFT_TO_RIGHT"
    }
  }
}
```

---

## SectionBreak

Divides the document into sections with independent formatting.

| Field | Type | Description |
|-------|------|-------------|
| `sectionStyle` | [`SectionStyle`](./05-styles.md#sectionstyle) | Section-level formatting (columns, headers/footers). |
| `suggestedInsertionIds[]` | string | Suggestion IDs proposing this insertion. |
| `suggestedDeletionIds[]` | string | Suggestion IDs proposing this deletion. |

---

## Table

A tabular data structure.

| Field | Type | Description |
|-------|------|-------------|
| `rows` | integer | Number of rows. |
| `columns` | integer | Number of columns. |
| `tableRows[]` | [`TableRow`](#tablerow) | Row content. |
| `tableStyle` | `TableStyle` | Table-level styling. |
| `suggestedInsertionIds[]` | string | Suggestion IDs proposing this insertion. |
| `suggestedDeletionIds[]` | string | Suggestion IDs proposing this deletion. |

### Sample Response

```json
{
  "startIndex": 593,
  "endIndex": 1234,
  "table": {
    "rows": 7,
    "columns": 3,
    "tableRows": [
      {
        "startIndex": 594,
        "endIndex": 637,
        "tableCells": [
          {
            "startIndex": 594,
            "endIndex": 604,
            "content": [
              {
                "startIndex": 595,
                "endIndex": 604,
                "paragraph": {
                  "elements": [
                    {
                      "startIndex": 595,
                      "endIndex": 604,
                      "textRun": {
                        "content": "Audience\n",
                        "textStyle": {
                          "bold": true,
                          "foregroundColor": {
                            "color": { "rgbColor": { "red": 1, "green": 1, "blue": 1 } }
                          }
                        }
                      }
                    }
                  ],
                  "paragraphStyle": { "namedStyleType": "NORMAL_TEXT", "alignment": "START" }
                }
              }
            ],
            "tableCellStyle": {
              "rowSpan": 1,
              "columnSpan": 1,
              "backgroundColor": {
                "color": { "rgbColor": { "red": 0.054, "green": 0.415, "blue": 0.929 } }
              },
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

> Shows a header row with white bold text on a blue background. The full table has 7 rows and 3 columns — only the first row's first cell is shown here.

### Sample Response — Table with Header Row and Fixed Column Widths

```json
{
  "startIndex": 547,
  "endIndex": 6282,
  "table": {
    "rows": 14,
    "columns": 6,
    "tableRows": [
      {
        "startIndex": 548,
        "endIndex": 609,
        "tableCells": [
          {
            "startIndex": 549,
            "endIndex": 558,
            "content": [
              {
                "startIndex": 550,
                "endIndex": 558,
                "paragraph": {
                  "elements": [
                    {
                      "startIndex": 550,
                      "endIndex": 558,
                      "textRun": {
                        "content": "Journey\n",
                        "textStyle": { "bold": true }
                      }
                    }
                  ]
                }
              }
            ]
          }
        ],
        "tableRowStyle": {
          "minRowHeight": { "unit": "PT" },
          "tableHeader": true
        }
      }
    ],
    "tableStyle": {
      "tableColumnProperties": [
        { "widthType": "FIXED_WIDTH", "width": { "magnitude": 69.75, "unit": "PT" } },
        { "widthType": "FIXED_WIDTH", "width": { "magnitude": 131.25, "unit": "PT" } },
        { "widthType": "FIXED_WIDTH", "width": { "magnitude": 86.25, "unit": "PT" } }
      ]
    }
  }
}
```

> A large 14×6 table spanning indices 547–6282. The first row uses `tableHeader: true` to designate it as a header row (repeats on each page). `tableColumnProperties` defines per-column widths with `FIXED_WIDTH` type. The `minRowHeight: { "unit": "PT" }` without a `magnitude` means zero minimum height (the row grows to fit content).

---

## TableRow

A row within a table.

| Field | Type | Description |
|-------|------|-------------|
| `startIndex` | integer | Zero-based start position. |
| `endIndex` | integer | Zero-based end position (exclusive). |
| `tableCells[]` | [`TableCell`](#tablecell) | Cells in this row. |
| `tableRowStyle` | [`TableRowStyle`](./05-styles.md#tablerowstyle) | Row-level styling. |
| `suggestedTableRowStyleChanges` | map<string, `SuggestedTableRowStyle`> | Suggested row style changes. |
| `suggestedInsertionIds[]` | string | Suggestion IDs. |
| `suggestedDeletionIds[]` | string | Suggestion IDs. |

---

## TableCell

A cell within a table row.

| Field | Type | Description |
|-------|------|-------------|
| `startIndex` | integer | Zero-based start position. |
| `endIndex` | integer | Zero-based end position (exclusive). |
| `content[]` | [`StructuralElement`](#structuralelement) | Cell content (paragraphs, nested tables). |
| `tableCellStyle` | [`TableCellStyle`](./05-styles.md#tablecellstyle) | Cell-level styling. |
| `suggestedTableCellStyleChanges` | map<string, `SuggestedTableCellStyle`> | Suggested cell style changes. |
| `suggestedInsertionIds[]` | string | Suggestion IDs. |
| `suggestedDeletionIds[]` | string | Suggestion IDs. |

---

## TableOfContents

An auto-generated table of contents.

| Field | Type | Description |
|-------|------|-------------|
| `content[]` | [`StructuralElement`](#structuralelement) | The TOC entries as structural elements. |

---

## Header

A page header section.

| Field | Type | Description |
|-------|------|-------------|
| `headerId` | string | Output only. Unique header identifier. |
| `content[]` | [`StructuralElement`](#structuralelement) | Header content. |

---

## Footer

A page footer section.

| Field | Type | Description |
|-------|------|-------------|
| `footerId` | string | Output only. Unique footer identifier. |
| `content[]` | [`StructuralElement`](#structuralelement) | Footer content. |

---

## Footnote

A footnote referenced from document content.

| Field | Type | Description |
|-------|------|-------------|
| `footnoteId` | string | Output only. Unique footnote identifier. |
| `content[]` | [`StructuralElement`](#structuralelement) | Footnote content. |
