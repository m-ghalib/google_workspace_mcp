# Paragraph Elements

Inline elements that compose a paragraph.

## ParagraphElement

An inline content element. Exactly one of the union fields will be set.

| Field | Type | Description |
|-------|------|-------------|
| `startIndex` | integer | Zero-based start position in UTF-16 code units. |
| `endIndex` | integer | Zero-based end position (exclusive). |

### Union field (one of):

| Field | Type | Description |
|-------|------|-------------|
| `textRun` | [`TextRun`](#textrun) | A run of styled text. |
| `autoText` | [`AutoText`](#autotext) | Auto-generated text (page numbers). |
| `pageBreak` | [`PageBreak`](#pagebreak) | A page break. |
| `columnBreak` | [`ColumnBreak`](#columnbreak) | A column break. |
| `footnoteReference` | [`FootnoteReference`](#footnotereference) | A reference to a footnote. |
| `horizontalRule` | [`HorizontalRule`](#horizontalrule) | A horizontal divider. |
| `equation` | [`Equation`](#equation) | A mathematical equation. |
| `inlineObjectElement` | [`InlineObjectElement`](#inlineobjectelement) | An inline embedded object. |
| `person` | [`Person`](#person) | A person mention (@-mention). |
| `richLink` | [`RichLink`](#richlink) | A smart chip link to a Google resource. |
| `dateElement` | [`DateElement`](#dateelement) | A smart date chip. |

---

## TextRun

A contiguous run of text with identical styling.

| Field | Type | Description |
|-------|------|-------------|
| `content` | string | The actual text content. |
| `textStyle` | [`TextStyle`](./05-styles.md#textstyle) | Character-level formatting. |
| `suggestedTextStyleChanges` | map<string, `SuggestedTextStyle`> | Suggested style changes keyed by suggestion ID. |
| `suggestedInsertionIds[]` | string | Suggestion IDs proposing this text was inserted. |
| `suggestedDeletionIds[]` | string | Suggestion IDs proposing this text be deleted. |

### Sample Response

```json
{
  "startIndex": 103,
  "endIndex": 138,
  "textRun": {
    "content": "Purpose & How to Use This Document\n",
    "textStyle": {
      "foregroundColor": {
        "color": {
          "rgbColor": { "red": 0.011764706, "green": 0.101960786, "blue": 0.42745098 }
        }
      },
      "fontSize": { "magnitude": 20, "unit": "PT" },
      "weightedFontFamily": { "fontFamily": "Poppins", "weight": 400 }
    }
  }
}
```

> A heading text run with custom font, size, and color. When `textStyle` is `{}` (empty), the text inherits its style from the paragraph's `namedStyleType`.

---

## AutoText

Dynamically generated text that updates automatically.

| Field | Type | Description |
|-------|------|-------------|
| `type` | enum [`AutoTextType`](./11-enums.md#autotexttype) | The type: `PAGE_NUMBER` or `PAGE_COUNT`. |
| `textStyle` | [`TextStyle`](./05-styles.md#textstyle) | Formatting applied to the auto text. |
| `suggestedTextStyleChanges` | map | Suggested style changes. |
| `suggestedInsertionIds[]` | string | Suggestion IDs. |
| `suggestedDeletionIds[]` | string | Suggestion IDs. |

---

## PageBreak

Forces content to continue on the next page.

| Field | Type | Description |
|-------|------|-------------|
| `textStyle` | [`TextStyle`](./05-styles.md#textstyle) | Formatting (inherited). |
| `suggestedTextStyleChanges` | map | Suggested style changes. |
| `suggestedInsertionIds[]` | string | Suggestion IDs. |
| `suggestedDeletionIds[]` | string | Suggestion IDs. |

---

## ColumnBreak

Forces content to continue in the next column.

| Field | Type | Description |
|-------|------|-------------|
| `textStyle` | [`TextStyle`](./05-styles.md#textstyle) | Formatting (inherited). |
| `suggestedTextStyleChanges` | map | Suggested style changes. |
| `suggestedInsertionIds[]` | string | Suggestion IDs. |
| `suggestedDeletionIds[]` | string | Suggestion IDs. |

---

## FootnoteReference

A pointer to a footnote from within the document body.

| Field | Type | Description |
|-------|------|-------------|
| `footnoteId` | string | The ID of the referenced footnote. |
| `footnoteNumber` | string | The rendered footnote number (e.g. "1", "2"). |
| `textStyle` | [`TextStyle`](./05-styles.md#textstyle) | Formatting. |
| `suggestedTextStyleChanges` | map | Suggested style changes. |
| `suggestedInsertionIds[]` | string | Suggestion IDs. |
| `suggestedDeletionIds[]` | string | Suggestion IDs. |

---

## HorizontalRule

A horizontal divider line.

| Field | Type | Description |
|-------|------|-------------|
| `textStyle` | [`TextStyle`](./05-styles.md#textstyle) | Formatting (inherited). |
| `suggestedTextStyleChanges` | map | Suggested style changes. |
| `suggestedInsertionIds[]` | string | Suggestion IDs. |
| `suggestedDeletionIds[]` | string | Suggestion IDs. |

---

## Equation

A mathematical equation rendered within the document.

| Field | Type | Description |
|-------|------|-------------|
| `textStyle` | [`TextStyle`](./05-styles.md#textstyle) | Formatting (inherited). |
| `suggestedInsertionIds[]` | string | Suggestion IDs. |
| `suggestedDeletionIds[]` | string | Suggestion IDs. |

---

## InlineObjectElement

A reference to an inline embedded object (image, chart, etc.).

| Field | Type | Description |
|-------|------|-------------|
| `inlineObjectId` | string | The ID of the inline object (key in `Document.inlineObjects`). |
| `textStyle` | [`TextStyle`](./05-styles.md#textstyle) | Formatting. |
| `suggestedTextStyleChanges` | map | Suggested style changes. |
| `suggestedInsertionIds[]` | string | Suggestion IDs. |
| `suggestedDeletionIds[]` | string | Suggestion IDs. |

---

## Person

A person mention (@-mention) smart chip.

| Field | Type | Description |
|-------|------|-------------|
| `personId` | string | Unique identifier for the person. |
| `personProperties` | [`PersonProperties`](#personproperties) | Name and email details. |
| `textStyle` | [`TextStyle`](./05-styles.md#textstyle) | Formatting. |
| `suggestedTextStyleChanges` | map | Suggested style changes. |
| `suggestedInsertionIds[]` | string | Suggestion IDs. |
| `suggestedDeletionIds[]` | string | Suggestion IDs. |

### PersonProperties

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Display name. |
| `email` | string | Email address. |

### Sample Response — Person Chip in Table Cell

```json
{
  "startIndex": 194,
  "endIndex": 195,
  "person": {
    "personId": "kix.xeznx9jz258t",
    "textStyle": {},
    "personProperties": {
      "name": "Vaidy Raghavan",
      "email": "vaidy.raghavan@xometry.com"
    }
  }
}
```

> Person chips occupy a single character position (startIndex 194, endIndex 195) but render as interactive chips showing the person's name. Multiple person chips can appear consecutively in a paragraph — for example, listing team members in a RACI table cell.

---

## RichLink

A smart chip linking to a Google Workspace resource.

| Field | Type | Description |
|-------|------|-------------|
| `richLinkId` | string | Unique identifier. |
| `richLinkProperties` | [`RichLinkProperties`](#richlinkproperties) | Link details. |
| `textStyle` | [`TextStyle`](./05-styles.md#textstyle) | Formatting. |
| `suggestedTextStyleChanges` | map | Suggested style changes. |
| `suggestedInsertionIds[]` | string | Suggestion IDs. |
| `suggestedDeletionIds[]` | string | Suggestion IDs. |

### RichLinkProperties

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Display title of the linked resource. |
| `uri` | string | URI of the linked resource. |
| `mimeType` | string | MIME type of the resource. |

---

## DateElement

A smart date chip that stores a timestamp and renders as locale-formatted text.

| Field | Type | Description |
|-------|------|-------------|
| `dateId` | string | Unique identifier for the date element. |
| `dateElementProperties` | [`DateElementProperties`](#dateelementproperties) | Date configuration and display. |
| `textStyle` | [`TextStyle`](./05-styles.md#textstyle) | Formatting. |
| `suggestedTextStyleChanges` | map | Suggested style changes. |
| `suggestedInsertionIds[]` | string | Suggestion IDs. |
| `suggestedDeletionIds[]` | string | Suggestion IDs. |

### DateElementProperties

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | string | ISO 8601 timestamp (e.g. `"2025-12-12T12:00:00Z"`). |
| `locale` | string | Language locale (e.g. `"en"`). |
| `dateFormat` | string | Date format enum (e.g. `DATE_FORMAT_MONTH_DAY_YEAR_ABBREVIATED`). |
| `timeFormat` | string | Time format enum (e.g. `TIME_FORMAT_DISABLED`). |
| `displayText` | string | The rendered display text (e.g. `"Dec 12, 2025"`). |

### Sample Response — Date Range with Inline Text

```json
{
  "startIndex": 864,
  "endIndex": 865,
  "dateElement": {
    "dateId": "kix.ufzz5692u4o",
    "textStyle": {},
    "dateElementProperties": {
      "timestamp": "2025-12-12T12:00:00Z",
      "locale": "en",
      "dateFormat": "DATE_FORMAT_MONTH_DAY_YEAR_ABBREVIATED",
      "timeFormat": "TIME_FORMAT_DISABLED",
      "displayText": "Dec 12, 2025"
    }
  }
}
```

> Like person chips, date elements occupy a single character position. The `displayText` is pre-rendered by Google based on the `dateFormat` and `locale` settings. The raw `timestamp` is always UTC ISO 8601.
