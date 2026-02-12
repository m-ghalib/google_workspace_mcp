# Common Types

Shared types used across multiple parts of the API.

## Range

A contiguous range of text within a document.

| Field | Type | Description |
|-------|------|-------------|
| `startIndex` | integer | Zero-based start position in UTF-16 code units. |
| `endIndex` | integer | Zero-based end position (exclusive). |
| `segmentId` | string | ID of the header, footer, or footnote. Empty string = body. |
| `tabId` | string | Tab containing the range. |

---

## Location

A specific position within the document.

| Field | Type | Description |
|-------|------|-------------|
| `index` | integer | Zero-based position in UTF-16 code units. |
| `segmentId` | string | ID of the header, footer, or footnote. Empty string = body. |
| `tabId` | string | Tab containing the position. |

---

## EndOfSegmentLocation

The end of a body, header, footer, or footnote.

| Field | Type | Description |
|-------|------|-------------|
| `segmentId` | string | ID of the segment. Empty string = body. |
| `tabId` | string | Tab containing the segment. |

---

## TableCellLocation

A specific cell within a table.

| Field | Type | Description |
|-------|------|-------------|
| `tableStartLocation` | [`Location`](#location) | Location of the table start. |
| `rowIndex` | integer | Zero-based row index. |
| `columnIndex` | integer | Zero-based column index. |

---

## TableRange

A range of cells within a table.

| Field | Type | Description |
|-------|------|-------------|
| `tableCellLocation` | [`TableCellLocation`](#tablecelllocation) | Top-left cell of the range. |
| `rowSpan` | integer | Number of rows in the range. |
| `columnSpan` | integer | Number of columns in the range. |

---

## SubstringMatchCriteria

Criteria for matching text in replace operations.

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | Text to search for. |
| `matchCase` | boolean | Whether the search is case-sensitive. |

---

## Dimension

A magnitude with a unit of measurement.

| Field | Type | Description |
|-------|------|-------------|
| `magnitude` | number | Numeric value. |
| `unit` | enum [`Unit`](./11-enums.md#unit) | Measurement unit (PT = points). |

### Sample Response

```json
{ "magnitude": 72, "unit": "PT" }
```

> 72 PT = 1 inch. Common values: margins (72 PT), font sizes (11 PT), padding (5 PT). When `magnitude` is 0, it may appear as just `{ "unit": "PT" }` with the magnitude omitted.

---

## OptionalColor

An optional color value. When unset, indicates transparency.

| Field | Type | Description |
|-------|------|-------------|
| `color` | [`Color`](#color) | The opaque color value. |

### Sample Response

```json
{
  "color": {
    "rgbColor": { "red": 0.054, "green": 0.415, "blue": 0.929 }
  }
}
```

> A blue color (table header background). An empty `{}` means transparent/unset — common for `backgroundColor` on unstyled text.

---

## Color

A solid color.

| Field | Type | Description |
|-------|------|-------------|
| `rgbColor` | [`RgbColor`](#rgbcolor) | RGB color value. |

---

## RgbColor

An RGB color with components from 0.0 to 1.0.

| Field | Type | Description |
|-------|------|-------------|
| `red` | number | Red component (0.0–1.0). |
| `green` | number | Green component (0.0–1.0). |
| `blue` | number | Blue component (0.0–1.0). |

### Sample Response

```json
{ "red": 0.011764706, "green": 0.101960786, "blue": 0.42745098 }
```

> A dark navy blue used for body text foreground color. Values range from 0.0 (none) to 1.0 (full intensity). Pure white = `{ "red": 1, "green": 1, "blue": 1 }`.

---

## Link

A hyperlink destination. Union field — exactly one of the following.

| Field | Type | Description |
|-------|------|-------------|
| `url` | string | External URL destination. |
| `tabId` | string | Document tab identifier. |
| `bookmark` | [`BookmarkLink`](#bookmarklink) | Bookmark reference. |
| `heading` | [`HeadingLink`](#headinglink) | Heading reference. |
| `bookmarkId` | string | **Deprecated.** Legacy bookmark ID. |
| `headingId` | string | **Deprecated.** Legacy heading ID. |

---

## BookmarkLink

Reference to a bookmark location.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | The bookmark's unique identifier. |
| `tabId` | string | The tab containing this bookmark. |

---

## HeadingLink

Reference to a heading location.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | The heading's unique identifier. |
| `tabId` | string | The tab containing this heading. |

---

## Bookmark

A bookmark within a document.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique bookmark identifier. |
| `name` | string | Display name. |
| `tableOfContentsRole` | string | Role in table of contents. |

---

## ObjectReferences

Container for multiple object identifiers.

| Field | Type | Description |
|-------|------|-------------|
| `objectIds[]` | string | IDs of referenced objects. |
