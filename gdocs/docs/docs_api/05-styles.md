# Styles & Formatting

All style types used across the Google Docs API.

## TextStyle

Character-level formatting applied to text runs.

| Field | Type | Description |
|-------|------|-------------|
| `bold` | boolean | Bold rendering. |
| `italic` | boolean | Italic rendering. |
| `underline` | boolean | Underline rendering. |
| `strikethrough` | boolean | Strikethrough rendering. |
| `smallCaps` | boolean | Small capitals rendering. |
| `backgroundColor` | [`OptionalColor`](./12-common-types.md#optionalcolor) | Text background color. |
| `foregroundColor` | [`OptionalColor`](./12-common-types.md#optionalcolor) | Text foreground color. |
| `fontSize` | [`Dimension`](./12-common-types.md#dimension) | Font size. |
| `weightedFontFamily` | [`WeightedFontFamily`](#weightedfontfamily) | Font family and weight. |
| `baselineOffset` | enum [`BaselineOffset`](./11-enums.md#baselineoffset) | Superscript/subscript. |
| `link` | [`Link`](./12-common-types.md#link) | Hyperlink destination. |

### Sample Response

```json
{
  "bold": true,
  "foregroundColor": {
    "color": { "rgbColor": { "red": 1, "green": 1, "blue": 1 } }
  }
}
```

> From a table header cell — only non-default fields appear. An empty `textStyle: {}` means the text inherits from its `namedStyleType`.

### Sample Response — Background Highlight

```json
{
  "bold": true,
  "italic": true,
  "backgroundColor": {
    "color": {
      "rgbColor": { "red": 1, "green": 0.9490196, "blue": 0.8 }
    }
  }
}
```

> Bold+italic text with a yellow highlight background (RGB ~255/242/204). Text background colors are distinct from paragraph shading — `backgroundColor` on `TextStyle` highlights specific text runs, while `Shading` on `ParagraphStyle` fills the entire paragraph width. An empty `backgroundColor: {}` means no highlight (transparent).

---

## WeightedFontFamily

Font specification with weight.

| Field | Type | Description |
|-------|------|-------------|
| `fontFamily` | string | Font name (from Google Docs or Google Fonts). |
| `weight` | integer | Font weight: 100–900 in multiples of 100. Default: 400. |

### Sample Response

```json
{
  "textStyle": {
    "weightedFontFamily": {
      "fontFamily": "Calibri",
      "weight": 400
    },
    "fontSize": {}
  }
}
```

> A text run using Calibri at normal weight (400). The empty `fontSize: {}` is a sparse field meaning "inherit font size from the named style" — distinct from omitting `fontSize` entirely, which means no override was explicitly set. Weight values: 100=Thin, 300=Light, 400=Normal, 700=Bold, 900=Black.

---

## ParagraphStyle

Paragraph-level formatting.

| Field | Type | Description |
|-------|------|-------------|
| `headingId` | string | Read-only. Heading identifier. |
| `namedStyleType` | enum [`NamedStyleType`](./11-enums.md#namedstyletype) | Named style (NORMAL_TEXT, HEADING_1, etc.). |
| `alignment` | enum [`Alignment`](./11-enums.md#alignment) | Text alignment. |
| `lineSpacing` | number | Line spacing as percentage (e.g. 100 = single, 200 = double). |
| `direction` | enum [`ContentDirection`](./11-enums.md#contentdirection) | Text direction. |
| `spacingMode` | enum [`SpacingMode`](./11-enums.md#spacingmode) | How paragraph spacing is handled. |
| `spaceAbove` | [`Dimension`](./12-common-types.md#dimension) | Space above paragraph. |
| `spaceBelow` | [`Dimension`](./12-common-types.md#dimension) | Space below paragraph. |
| `borderBetween` | [`ParagraphBorder`](#paragraphborder) | Border between this and adjacent paragraphs with same style. |
| `borderTop` | [`ParagraphBorder`](#paragraphborder) | Top border. |
| `borderBottom` | [`ParagraphBorder`](#paragraphborder) | Bottom border. |
| `borderLeft` | [`ParagraphBorder`](#paragraphborder) | Left border. |
| `borderRight` | [`ParagraphBorder`](#paragraphborder) | Right border. |
| `indentFirstLine` | [`Dimension`](./12-common-types.md#dimension) | First line indentation. |
| `indentStart` | [`Dimension`](./12-common-types.md#dimension) | Start-side indentation. |
| `indentEnd` | [`Dimension`](./12-common-types.md#dimension) | End-side indentation. |
| `tabStops[]` | [`TabStop`](#tabstop) | Read-only. Custom tab stops. |
| `keepLinesTogether` | boolean | Keep all lines on same page/column. |
| `keepWithNext` | boolean | Keep with the next paragraph. |
| `avoidWidowAndOrphan` | boolean | Avoid widow/orphan lines. |
| `shading` | [`Shading`](#shading) | Paragraph background shading. |
| `pageBreakBefore` | boolean | Start paragraph on a new page. |

### Sample Response

```json
{
  "headingId": "h.i9dx5sbhk9zn",
  "namedStyleType": "HEADING_1",
  "direction": "LEFT_TO_RIGHT",
  "spaceAbove": { "magnitude": 12, "unit": "PT" },
  "spaceBelow": { "magnitude": 6, "unit": "PT" }
}
```

> A `HEADING_1` paragraph — only overridden fields appear. Default-valued fields (alignment, borders, indents) are omitted by the API.

---

## ParagraphBorder

Border applied to a paragraph edge.

| Field | Type | Description |
|-------|------|-------------|
| `color` | [`OptionalColor`](./12-common-types.md#optionalcolor) | Border color. |
| `dashStyle` | enum [`DashStyle`](./11-enums.md#dashstyle) | Line pattern. |
| `padding` | [`Dimension`](./12-common-types.md#dimension) | Space between text and border. |
| `width` | [`Dimension`](./12-common-types.md#dimension) | Border thickness. |

---

## Shading

Paragraph background shading.

| Field | Type | Description |
|-------|------|-------------|
| `backgroundColor` | [`OptionalColor`](./12-common-types.md#optionalcolor) | Background color. |

---

## TabStop

A fixed position for text alignment within a paragraph.

| Field | Type | Description |
|-------|------|-------------|
| `offset` | [`Dimension`](./12-common-types.md#dimension) | Distance from paragraph start margin. |
| `alignment` | enum [`TabStopAlignment`](./11-enums.md#tabstopalignment) | Alignment at this stop. |

---

## DocumentStyle

Document-wide formatting settings.

| Field | Type | Description |
|-------|------|-------------|
| `background` | [`Background`](#background) | Document background. |
| `defaultHeaderId` | string | Default header ID. |
| `defaultFooterId` | string | Default footer ID. |
| `evenPageHeaderId` | string | Even-page header ID. |
| `evenPageFooterId` | string | Even-page footer ID. |
| `firstPageHeaderId` | string | First-page header ID. |
| `firstPageFooterId` | string | First-page footer ID. |
| `documentFormat` | enum `DocumentFormat` | Document format type. |
| `documentMode` | enum `DocumentMode` | Document mode. |

### Sample Response

```json
{
  "background": { "color": {} },
  "pageNumberStart": 1,
  "marginTop": { "magnitude": 72, "unit": "PT" },
  "marginBottom": { "magnitude": 72, "unit": "PT" },
  "marginRight": { "magnitude": 72, "unit": "PT" },
  "marginLeft": { "magnitude": 72, "unit": "PT" },
  "pageSize": {
    "height": { "magnitude": 792, "unit": "PT" },
    "width": { "magnitude": 612, "unit": "PT" }
  },
  "marginHeader": { "magnitude": 36, "unit": "PT" },
  "marginFooter": { "magnitude": 36, "unit": "PT" },
  "useCustomHeaderFooterMargins": true,
  "documentFormat": { "documentMode": "PAGELESS" }
}
```

> A pageless document with US Letter dimensions (612 x 792 PT = 8.5" x 11") and 1-inch margins. Empty `background.color` means white.

---

## Background

Document background.

| Field | Type | Description |
|-------|------|-------------|
| `color` | [`OptionalColor`](./12-common-types.md#optionalcolor) | Solid background color. |

---

## NamedStyles

Container for all named style definitions.

| Field | Type | Description |
|-------|------|-------------|
| `styles[]` | [`NamedStyle`](#namedstyle) | Collection of named styles. |

---

## NamedStyle

A predefined style (e.g. HEADING_1, NORMAL_TEXT).

| Field | Type | Description |
|-------|------|-------------|
| `namedStyleType` | enum [`NamedStyleType`](./11-enums.md#namedstyletype) | Style type identifier. |
| `displayName` | string | User-visible name. |
| `textStyle` | [`TextStyle`](#textstyle) | Text formatting. |
| `paragraphStyle` | [`ParagraphStyle`](#paragraphstyle) | Paragraph formatting. |

### Sample Response

```json
{
  "namedStyleType": "NORMAL_TEXT",
  "textStyle": {
    "bold": false,
    "italic": false,
    "underline": false,
    "strikethrough": false,
    "smallCaps": false,
    "backgroundColor": {},
    "foregroundColor": {
      "color": { "rgbColor": { "red": 0.011764706, "green": 0.101960786, "blue": 0.42745098 } }
    },
    "fontSize": { "magnitude": 11, "unit": "PT" },
    "weightedFontFamily": { "fontFamily": "Poppins", "weight": 400 },
    "baselineOffset": "NONE"
  },
  "paragraphStyle": {
    "namedStyleType": "NORMAL_TEXT",
    "alignment": "START",
    "lineSpacing": 115,
    "direction": "LEFT_TO_RIGHT",
    "spacingMode": "COLLAPSE_LISTS",
    "avoidWidowAndOrphan": true,
    "keepLinesTogether": false,
    "keepWithNext": false,
    "pageBreakBefore": false
  }
}
```

> The `NORMAL_TEXT` base style — all 9 named styles (TITLE, SUBTITLE, HEADING_1–6, NORMAL_TEXT) follow this structure. Named styles define full defaults; individual paragraphs override only specific fields.

---

## SectionStyle

Section-level formatting controlling multi-column layout and headers/footers.

| Field | Type | Description |
|-------|------|-------------|
| `columnProperties[]` | [`SectionColumnProperties`](#sectioncolumnproperties) | Column configuration. |
| `defaultHeaderId` | string | Default header ID for this section. |
| `defaultFooterId` | string | Default footer ID for this section. |
| `evenPageHeaderId` | string | Even-page header ID. |
| `evenPageFooterId` | string | Even-page footer ID. |
| `firstPageHeaderId` | string | First-page header ID. |
| `firstPageFooterId` | string | First-page footer ID. |
| `sectionType` | enum [`SectionType`](./11-enums.md#sectiontype) | Section break type. |

---

## SectionColumnProperties

Column layout configuration.

| Field | Type | Description |
|-------|------|-------------|
| `columnSeparatorStyle` | enum [`ColumnSeparatorStyle`](./11-enums.md#columnseparatorstyle) | Visual divider style. |
| `columnCount` | integer | Number of columns (minimum 1). |

---

## TableCellStyle

Cell-level formatting within a table.

| Field | Type | Description |
|-------|------|-------------|
| `paddingTop` | [`Dimension`](./12-common-types.md#dimension) | Top padding. |
| `paddingBottom` | [`Dimension`](./12-common-types.md#dimension) | Bottom padding. |
| `paddingLeft` | [`Dimension`](./12-common-types.md#dimension) | Left padding. |
| `paddingRight` | [`Dimension`](./12-common-types.md#dimension) | Right padding. |
| `borderTop` | [`TableCellBorder`](#tablecellborder) | Top border. |
| `borderBottom` | [`TableCellBorder`](#tablecellborder) | Bottom border. |
| `borderLeft` | [`TableCellBorder`](#tablecellborder) | Left border. |
| `borderRight` | [`TableCellBorder`](#tablecellborder) | Right border. |
| `backgroundColor` | [`OptionalColor`](./12-common-types.md#optionalcolor) | Cell background color. |
| `contentAlignment` | enum [`ContentAlignment`](./11-enums.md#contentalignment) | Vertical content alignment. |
| `columnSpan` | integer | Columns spanned by this cell. |
| `rowSpan` | integer | Rows spanned by this cell. |

### Sample Response

```json
{
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
```

> A table header cell with blue background and 5pt padding on all sides. Note: `borderTop/Bottom/Left/Right` are omitted here because the table uses default borders.

---

## TableCellBorder

Border applied to a table cell edge.

| Field | Type | Description |
|-------|------|-------------|
| `color` | [`OptionalColor`](./12-common-types.md#optionalcolor) | Border color. |
| `dashStyle` | enum [`DashStyle`](./11-enums.md#dashstyle) | Line pattern. |
| `width` | [`Dimension`](./12-common-types.md#dimension) | Border thickness. |

---

## TableRowStyle

Row-level formatting within a table.

| Field | Type | Description |
|-------|------|-------------|
| `minHeight` | [`Dimension`](./12-common-types.md#dimension) | Minimum row height. |
| `exactHeight` | [`Dimension`](./12-common-types.md#dimension) | Exact row height. |
| `tableHeader` | boolean | Whether this row is a header row. |

---

## TableColumnProperties

Column-level properties within a table.

| Field | Type | Description |
|-------|------|-------------|
| `width` | [`Dimension`](./12-common-types.md#dimension) | Column width. |
| `widthType` | enum [`WidthType`](./11-enums.md#widthtype) | Width measurement type. |
