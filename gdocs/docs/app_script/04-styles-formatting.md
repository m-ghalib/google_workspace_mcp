# Styles & Formatting

Comparison of styling capabilities between Google Apps Script and Google Docs REST API.

## Formatting Paradigm Comparison

### Apps Script: Method-Based Styling

Apps Script uses setter/getter methods on element objects. Styling is applied **in-place** — calling a method immediately modifies the document:

```javascript
// Text formatting
var text = paragraph.editAsText();
text.setBold(true);
text.setFontSize(14);
text.setForegroundColor("#FF0000");

// Paragraph formatting
paragraph.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
paragraph.setSpacingBefore(12);
```

**Key characteristics:**
- **Immediate mutation**: Each method call directly modifies the document
- **Method chaining**: Most methods return the element for chaining
- **Range-based operations**: Most methods support full element or character offset ranges
- **Mixed model**: Some properties use enums (`HorizontalAlignment`), others use primitives (`number`, `string`)

### REST API: Style Objects with Field Masks

REST API uses style objects passed to `batchUpdate` requests. Styling is **declarative** — you describe the desired end state:

```json
{
  "requests": [
    {
      "updateTextStyle": {
        "range": { "startIndex": 1, "endIndex": 10 },
        "textStyle": {
          "bold": true,
          "fontSize": { "magnitude": 14, "unit": "PT" },
          "foregroundColor": { "color": { "rgbColor": { "red": 1 } } }
        },
        "fields": "bold,fontSize,foregroundColor"
      }
    },
    {
      "updateParagraphStyle": {
        "range": { "startIndex": 1, "endIndex": 10 },
        "paragraphStyle": {
          "alignment": "CENTER",
          "spaceAbove": { "magnitude": 12, "unit": "PT" }
        },
        "fields": "alignment,spaceAbove"
      }
    }
  ]
}
```

**Key characteristics:**
- **Batch operations**: Multiple style changes in a single request
- **Field masks required**: Must specify which fields to update via `fields` parameter
- **Structured types**: Complex nested objects for colors, dimensions, etc.
- **Partial updates**: Only specified fields are modified; others remain unchanged
- **Suggestion support**: Can create suggested changes instead of direct edits

## Text Style Comparison

Character-level formatting applied to text runs.

| Formatting Property | Apps Script Method | REST API Field | Notes |
|--------------------|--------------------|---------------|-------|
| **Bold** | `Text.setBold(bool)` / `isBold()` | `TextStyle.bold` | Equivalent |
| **Italic** | `Text.setItalic(bool)` / `isItalic()` | `TextStyle.italic` | Equivalent |
| **Underline** | `Text.setUnderline(bool)` / `isUnderline()` | `TextStyle.underline` | Equivalent |
| **Strikethrough** | `Text.setStrikethrough(bool)` / `isStrikethrough()` | `TextStyle.strikethrough` | Equivalent |
| **Font Family** | `Text.setFontFamily(string)` / `getFontFamily()` | `TextStyle.weightedFontFamily.fontFamily` | REST API includes weight |
| **Font Size** | `Text.setFontSize(number)` / `getFontSize()` | `TextStyle.fontSize.magnitude` | REST API uses `Dimension` object |
| **Text Color** | `Text.setForegroundColor(string)` / `getForegroundColor()` | `TextStyle.foregroundColor.color` | REST API uses `OptionalColor` object |
| **Background Color** | `Text.setBackgroundColor(string)` / `getBackgroundColor()` | `TextStyle.backgroundColor.color` | REST API uses `OptionalColor` object |
| **Hyperlink** | `Text.setLinkUrl(string)` / `getLinkUrl()` | `TextStyle.link.url` | REST API supports bookmarks too |
| **Baseline Offset** | `Text.setTextAlignment(enum)` / `getTextAlignment()` | `TextStyle.baselineOffset` | Superscript/subscript positioning |
| **Small Caps** | ❌ | `TextStyle.smallCaps` | **REST API only** |
| **Font Weight** | ❌ | `TextStyle.weightedFontFamily.weight` | **REST API only** (100–900) |

### Apps Script Only
- `Text.getTextAttributeIndices()` — Returns indices where formatting changes (no REST API equivalent)

### REST API Only
- **Small caps rendering**: `TextStyle.smallCaps` — not available in Apps Script
- **Explicit font weight**: `TextStyle.weightedFontFamily.weight` — Apps Script uses font family names that imply weight (e.g., "Arial Bold")
- **Suggestion tracking**: `suggestedTextStyleChanges`, `suggestedInsertionIds`, `suggestedDeletionIds` — no Apps Script equivalent

## Paragraph Style Comparison

Paragraph-level formatting.

| Formatting Property | Apps Script Method | REST API Field | Notes |
|--------------------|--------------------|---------------|-------|
| **Alignment** | `Paragraph.setAlignment(enum)` / `getAlignment()` | `ParagraphStyle.alignment` | Same concept, different enum names |
| **Line Spacing** | `Paragraph.setLineSpacing(number)` / `getLineSpacing()` | `ParagraphStyle.lineSpacing` | Apps Script uses multiplier (1.5 = 150), REST API uses percentage (150) |
| **Text Direction** | `Paragraph.setLeftToRight(bool)` / `isLeftToRight()` | `ParagraphStyle.direction` | Apps Script boolean, REST API enum |
| **Space Above** | `Paragraph.setSpacingBefore(number)` / `getSpacingBefore()` | `ParagraphStyle.spaceAbove.magnitude` | REST API uses `Dimension` object |
| **Space Below** | `Paragraph.setSpacingAfter(number)` / `getSpacingAfter()` | `ParagraphStyle.spaceBelow.magnitude` | REST API uses `Dimension` object |
| **First Line Indent** | `Paragraph.setIndentFirstLine(number)` / `getIndentFirstLine()` | `ParagraphStyle.indentFirstLine.magnitude` | REST API uses `Dimension` object |
| **Start Indent** | `Paragraph.setIndentStart(number)` / `getIndentStart()` | `ParagraphStyle.indentStart.magnitude` | REST API uses `Dimension` object |
| **End Indent** | `Paragraph.setIndentEnd(number)` / `getIndentEnd()` | `ParagraphStyle.indentEnd.magnitude` | REST API uses `Dimension` object |
| **Heading Style** | `Paragraph.setHeading(enum)` / `getHeading()` | `ParagraphStyle.namedStyleType` | Maps to named styles (HEADING_1, etc.) |
| **Heading ID** | ❌ | `ParagraphStyle.headingId` | **REST API only** (read-only) |
| **Borders** | ❌ | `ParagraphStyle.border{Top,Bottom,Left,Right,Between}` | **REST API only** |
| **Shading** | ❌ | `ParagraphStyle.shading.backgroundColor` | **REST API only** (paragraph background) |
| **Spacing Mode** | ❌ | `ParagraphStyle.spacingMode` | **REST API only** (COLLAPSE_LISTS, etc.) |
| **Tab Stops** | ❌ | `ParagraphStyle.tabStops[]` | **REST API only** (read-only) |
| **Keep Together** | ❌ | `ParagraphStyle.keepLinesTogether` | **REST API only** |
| **Keep With Next** | ❌ | `ParagraphStyle.keepWithNext` | **REST API only** |
| **Avoid Widow/Orphan** | ❌ | `ParagraphStyle.avoidWidowAndOrphan` | **REST API only** |
| **Page Break Before** | ❌ | `ParagraphStyle.pageBreakBefore` | **REST API only** |

### Apps Script Only
- `Paragraph.setTextAlignment(enum)` / `getTextAlignment()` — Duplicates text baseline alignment (also on Text element)

### REST API Only
- **Paragraph borders**: Full border control (top, bottom, left, right, between) with color, width, dash style, and padding — not available in Apps Script
- **Paragraph shading**: Background color distinct from text highlighting — not available in Apps Script
- **Advanced layout controls**: Keep together, keep with next, avoid widow/orphan, page break before — not available in Apps Script
- **Spacing mode**: Control how spacing collapses in lists — not available in Apps Script
- **Heading IDs**: Read-only identifiers for cross-referencing headings — not available in Apps Script

## Table Style Comparison

### Table Cell Formatting

| Formatting Property | Apps Script Method | REST API Field | Notes |
|--------------------|--------------------|---------------|-------|
| **Background Color** | `TableCell.setBackgroundColor(string)` / `getBackgroundColor()` | `TableCellStyle.backgroundColor.color` | Equivalent |
| **Padding Top** | `TableCell.setPaddingTop(number)` / `getPaddingTop()` | `TableCellStyle.paddingTop.magnitude` | REST API uses `Dimension` object |
| **Padding Bottom** | `TableCell.setPaddingBottom(number)` / `getPaddingBottom()` | `TableCellStyle.paddingBottom.magnitude` | REST API uses `Dimension` object |
| **Padding Left** | `TableCell.setPaddingLeft(number)` / `getPaddingLeft()` | `TableCellStyle.paddingLeft.magnitude` | REST API uses `Dimension` object |
| **Padding Right** | `TableCell.setPaddingRight(number)` / `getPaddingRight()` | `TableCellStyle.paddingRight.magnitude` | REST API uses `Dimension` object |
| **Vertical Alignment** | `TableCell.setVerticalAlignment(enum)` / `getVerticalAlignment()` | `TableCellStyle.contentAlignment` | Different enum names |
| **Column Span** | `TableCell.getColSpan()` (read-only) | `TableCellStyle.columnSpan` | Equivalent |
| **Row Span** | `TableCell.getRowSpan()` (read-only) | `TableCellStyle.rowSpan` | Equivalent |
| **Cell Width** | `TableCell.setWidth(number)` / `getWidth()` | `TableColumnProperties.width.magnitude` | Apps Script sets column width from cell |
| **Borders** | ❌ | `TableCellStyle.border{Top,Bottom,Left,Right}` | **REST API only** |

### Table Row Formatting

| Formatting Property | Apps Script Method | REST API Field | Notes |
|--------------------|--------------------|---------------|-------|
| **Minimum Height** | ❌ | `TableRowStyle.minHeight.magnitude` | **REST API only** |
| **Exact Height** | ❌ | `TableRowStyle.exactHeight.magnitude` | **REST API only** |
| **Header Row** | ❌ | `TableRowStyle.tableHeader` | **REST API only** |

### REST API Only
- **Cell borders**: Individual border control per edge with color, width, and dash style — not available in Apps Script
- **Row height constraints**: Minimum and exact height settings — not available in Apps Script
- **Header row designation**: Mark rows as table headers for repeat printing — not available in Apps Script

## Document Style Comparison

Document-wide formatting settings.

| Formatting Property | Apps Script Method | REST API Field | Notes |
|--------------------|--------------------|---------------|-------|
| **Page Width** | `Body.setPageWidth(number)` / `getPageWidth()` | `DocumentStyle.pageSize.width.magnitude` | REST API uses nested `Size` object |
| **Page Height** | `Body.setPageHeight(number)` / `getPageHeight()` | `DocumentStyle.pageSize.height.magnitude` | REST API uses nested `Size` object |
| **Margin Top** | `Body.setMarginTop(number)` / `getMarginTop()` | `DocumentStyle.marginTop.magnitude` | REST API uses `Dimension` object |
| **Margin Bottom** | `Body.setMarginBottom(number)` / `getMarginBottom()` | `DocumentStyle.marginBottom.magnitude` | REST API uses `Dimension` object |
| **Margin Left** | `Body.setMarginLeft(number)` / `getMarginLeft()` | `DocumentStyle.marginLeft.magnitude` | REST API uses `Dimension` object |
| **Margin Right** | `Body.setMarginRight(number)` / `getMarginRight()` | `DocumentStyle.marginRight.magnitude` | REST API uses `Dimension` object |
| **Background Color** | ❌ | `DocumentStyle.background.color` | **REST API only** |
| **Header/Footer IDs** | ❌ | `DocumentStyle.{default,evenPage,firstPage}{Header,Footer}Id` | **REST API only** |
| **Header/Footer Margins** | ❌ | `DocumentStyle.margin{Header,Footer}.magnitude` | **REST API only** |
| **Custom Header/Footer Margins** | ❌ | `DocumentStyle.useCustomHeaderFooterMargins` | **REST API only** |
| **Page Number Start** | ❌ | `DocumentStyle.pageNumberStart` | **REST API only** |
| **Document Mode** | ❌ | `DocumentStyle.documentFormat.documentMode` | **REST API only** (PAGELESS, etc.) |

### Apps Script Only
- `Body.setTextAlignment(enum)` / `getTextAlignment()` — Applies alignment to entire body (no direct REST API equivalent)

### REST API Only
- **Document background**: Solid color background for entire document — not available in Apps Script
- **Header/footer system**: Complex header/footer management with different headers for first page, even pages, and default — not directly accessible in Apps Script
- **Custom header/footer margins**: Separate margin control for headers and footers — not available in Apps Script
- **Page numbering**: Control starting page number — not available in Apps Script
- **Document mode**: Pageless vs. paginated layout — not available in Apps Script

## List Style Comparison

| Formatting Property | Apps Script Method | REST API Field | Notes |
|--------------------|--------------------|---------------|-------|
| **Glyph Type** | `ListItem.setGlyphType(enum)` / `getGlyphType()` | `Bullet.glyph.glyphType` (read-only) | Apps Script can set, REST API read-only |
| **Nesting Level** | `ListItem.setNestingLevel(number)` / `getNestingLevel()` | `Paragraph.bullet.nestingLevel` | Equivalent |
| **List ID** | `ListItem.getListId()` (read-only) | `Paragraph.bullet.listId` | Both read-only |
| **Bullet Presets** | ❌ | `CreateParagraphBulletsRequest.bulletPreset` | **REST API only** (BULLET_DISC_CIRCLE_SQUARE, etc.) |
| **Custom Glyph** | ❌ | `Bullet.glyph.customGlyphSymbol` | **REST API only** |

### REST API Only
- **Bullet presets**: Pre-configured bullet styles with nesting patterns — not available in Apps Script (must manually configure each level)
- **Custom glyph symbols**: Arbitrary Unicode characters as bullets — not available in Apps Script
- **Bullet alignment**: Horizontal positioning of bullets independent of text — not available in Apps Script

## Attribute-Based Formatting (Apps Script)

Apps Script provides a unified attribute system via the `Attribute` enum. The `setAttributes(object)` / `getAttributes()` methods accept/return objects with enum keys:

```javascript
var attributes = {};
attributes[DocumentApp.Attribute.BOLD] = true;
attributes[DocumentApp.Attribute.FONT_SIZE] = 14;
attributes[DocumentApp.Attribute.FOREGROUND_COLOR] = "#FF0000";

text.setAttributes(attributes);
```

**Coverage of Attribute enum:**
- ✅ **Text properties**: BOLD, ITALIC, UNDERLINE, STRIKETHROUGH, FONT_FAMILY, FONT_SIZE, FOREGROUND_COLOR, BACKGROUND_COLOR, LINK_URL
- ✅ **Paragraph properties**: HEADING, HORIZONTAL_ALIGNMENT, LINE_SPACING, SPACING_BEFORE, SPACING_AFTER, INDENT_START, INDENT_END, INDENT_FIRST_LINE, LEFT_TO_RIGHT
- ✅ **List properties**: GLYPH_TYPE, LIST_ID, NESTING_LEVEL
- ✅ **Table properties**: BORDER_COLOR, BORDER_WIDTH, PADDING_TOP, PADDING_BOTTOM, PADDING_LEFT, PADDING_RIGHT, VERTICAL_ALIGNMENT, WIDTH, MINIMUM_HEIGHT
- ✅ **Document properties**: PAGE_WIDTH, PAGE_HEIGHT, MARGIN_TOP, MARGIN_BOTTOM, MARGIN_LEFT, MARGIN_RIGHT
- ✅ **Inline properties**: HEIGHT (for images), CODE (for equations)

The `Attribute` enum is the **master list** of all formatting attributes in Apps Script. It combines text, paragraph, table, and document-level properties into a single namespace.

## Coverage Summary

### REST API Capabilities NOT in Apps Script

1. **Small caps**: `TextStyle.smallCaps` — render text in small capital letters
2. **Explicit font weight**: `TextStyle.weightedFontFamily.weight` — fine-grained weight control (100–900)
3. **Paragraph borders**: Full border system with color, width, dash style, and padding on all four edges
4. **Paragraph shading**: Background color distinct from text highlighting
5. **Advanced layout controls**: Keep lines together, keep with next paragraph, avoid widow/orphan lines, force page break before
6. **Spacing mode**: Control how spacing collapses between list items
7. **Heading IDs**: Read-only identifiers for cross-referencing (generated by API)
8. **Tab stops**: Custom tab stop positions with alignment (read-only in API)
9. **Table cell borders**: Individual border control per cell edge
10. **Table row height**: Minimum and exact height constraints
11. **Table header rows**: Mark rows as headers for repeat printing
12. **Document background**: Solid color background for entire document
13. **Header/footer system**: Complex management with first page, even pages, and default headers/footers
14. **Custom header/footer margins**: Separate margin control for headers/footers
15. **Page numbering**: Control starting page number
16. **Document mode**: Pageless vs. paginated layout
17. **Bullet presets**: Pre-configured bullet styles with multi-level nesting patterns
18. **Custom glyph symbols**: Arbitrary Unicode characters as bullets
19. **Bullet alignment**: Horizontal positioning of bullets independent of text
20. **Suggestion tracking**: Create suggested changes instead of direct edits
21. **Field masks**: Partial update control — specify exactly which fields to modify

### Apps Script Capabilities NOT in REST API

1. **Text attribute indices**: `Text.getTextAttributeIndices()` — find where formatting changes occur
2. **Unified attribute system**: Single `Attribute` enum + `setAttributes()`/`getAttributes()` methods for all formatting types
3. **In-place mutation**: Direct modification without batch requests
4. **Range-based operations**: Apply formatting to character ranges within a single method call
5. **Method chaining**: Return element for fluent API style

### Key Paradigm Differences

| Aspect | Apps Script | REST API |
|--------|-------------|----------|
| **Modification model** | In-place mutation | Batch requests with declarative style objects |
| **Update granularity** | Per-property methods | Field masks for partial updates |
| **Type system** | Mix of primitives, enums, and strings | Structured nested objects |
| **Operation cost** | N method calls = N mutations | N changes in 1 batch = 1 request |
| **Formatting discovery** | `getTextAttributeIndices()` finds boundaries | No equivalent (must traverse structure) |
| **Suggestion support** | None | Full suggestion tracking system |
| **Color format** | Hex strings (`"#FF0000"`) | Nested RGB objects (`{ rgbColor: { red: 1 } }`) |
| **Dimensions** | Raw numbers (points) | `Dimension` objects (`{ magnitude: 12, unit: "PT" }`) |
| **Default handling** | Methods set all properties | Field masks enable sparse updates |

### Formatting Power Ranking

1. **REST API**: Most powerful — full access to all formatting capabilities, suggestion system, and fine-grained control
2. **Apps Script**: Good coverage for common formatting tasks, but missing advanced layout features and suggestion tracking

The REST API is more verbose but significantly more powerful. Apps Script is more convenient for simple formatting tasks but hits limitations quickly with advanced layout requirements.
