# Structural Elements — Apps Script API

Block-level container and element classes for document structure. These classes provide tree-based DOM-like navigation and manipulation, contrasting with the REST API's flat index-based addressing.

---

## Architecture Comparison: Tree vs. Flat Index

### Apps Script Approach: DOM-Like Tree Navigation
- **Hierarchical references**: `body.getChild(0).asTable().getRow(2).getCell(1)`
- **Parent-child relationships**: `element.getParent()`, `element.getNextSibling()`
- **Convenience methods**: `body.appendParagraph("text")` creates and appends in one call
- **In-place mutation**: Methods modify the document immediately without explicit batch requests

### REST API Approach: Flat Index-Based Addressing
- **Linear addressing**: All content addressed by zero-based UTF-16 code unit indices
- **No direct references**: Must track `startIndex`/`endIndex` positions
- **Atomic operations**: Must compose multiple `batchUpdate` requests for complex changes
- **Batch submission**: All changes bundled and submitted in a single API call

### Key Difference
Apps Script lets you navigate like a DOM tree (`getChild`, `getParent`, `appendParagraph`), while REST API requires calculating text positions and composing batch request arrays.

---

## Body

The main content container of a document tab. In Apps Script, Body extends `ContainerElement` and provides methods for content creation, retrieval, and page formatting.

**REST API Equivalent**: The `Body` resource (see [docs_api/03-structural-elements.md](../docs_api/03-structural-elements.md#body)) contains a `content[]` array of `StructuralElement` objects indexed by position.

### Content Creation Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `appendHorizontalRule()` | HorizontalRule | `InsertTextRequest` + `UpdateParagraphStyleRequest` | Insert `\n` and apply horizontal rule styling |
| `appendImage(BlobSource)` | InlineImage | `InsertInlineImageRequest` | Append image at end of body |
| `appendImage(InlineImage)` | InlineImage | `InsertInlineImageRequest` | Clone and append existing image |
| `appendListItem(String)` | ListItem | `InsertTextRequest` + `CreateParagraphBulletsRequest` | Create paragraph, convert to list item |
| `appendListItem(ListItem)` | ListItem | Multiple batch requests | Copy list item structure with bullet formatting |
| `appendPageBreak()` | PageBreak | `InsertPageBreakRequest` | Insert at `endOfSegmentLocation` |
| `appendPageBreak(PageBreak)` | PageBreak | `InsertPageBreakRequest` | Clone and append page break |
| `appendParagraph(String)` | Paragraph | `InsertTextRequest` | Insert text followed by `\n` |
| `appendParagraph(Paragraph)` | Paragraph | Multiple batch requests | Copy paragraph content and style |
| `appendTable()` | Table | `InsertTableRequest` | Create empty 1×1 table |
| `appendTable(String[][])` | Table | `InsertTableRequest` + multiple `InsertTextRequest` | Create table and populate cells |
| `appendTable(Table)` | Table | `InsertTableRequest` + multiple style/content requests | Clone table structure |

### Content Insertion Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `insertHorizontalRule(Integer)` | HorizontalRule | `InsertTextRequest` + style requests | Insert at child index |
| `insertImage(Integer, BlobSource)` | InlineImage | `InsertInlineImageRequest` | Insert at specific position |
| `insertImage(Integer, InlineImage)` | InlineImage | `InsertInlineImageRequest` | Clone at position |
| `insertListItem(Integer, String)` | ListItem | `InsertTextRequest` + `CreateParagraphBulletsRequest` | Insert and convert to list |
| `insertListItem(Integer, ListItem)` | ListItem | Multiple batch requests | Clone list item at position |
| `insertPageBreak(Integer)` | PageBreak | `InsertPageBreakRequest` | Insert at child index |
| `insertPageBreak(Integer, PageBreak)` | PageBreak | `InsertPageBreakRequest` | Clone at position |
| `insertParagraph(Integer, String)` | Paragraph | `InsertTextRequest` | Insert at child index |
| `insertParagraph(Integer, Paragraph)` | Paragraph | Multiple batch requests | Clone at position |
| `insertTable(Integer)` | Table | `InsertTableRequest` | Empty 1×1 table at position |
| `insertTable(Integer, String[][])` | Table | `InsertTableRequest` + content requests | Populated table at position |
| `insertTable(Integer, Table)` | Table | Multiple batch requests | Clone table at position |

### Content Retrieval Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getChild(Integer)` | Element | Navigate `Body.content[]` array | Access child by index |
| `getImages()` | InlineImage[] | Filter `ParagraphElement` for `inlineObjectElement` | Search all paragraphs |
| `getListItems()` | ListItem[] | Filter `Paragraph` objects with `bullet` field | Find all list items |
| `getParagraphs()` | Paragraph[] | Filter `StructuralElement` for `paragraph` union field | Get all paragraphs |
| `getTables()` | Table[] | Filter `StructuralElement` for `table` union field | Get all tables |
| `getText()` | String | Aggregate all `textRun.content` fields | Concatenate text content |
| `getNumChildren()` | Integer | `Body.content.length` | Count structural elements |

### Text Manipulation Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `editAsText()` | Text | Convert to text interface | Enables character-level operations |
| `findText(String)` | RangeElement | Search across all `textRun.content` | Regex pattern search |
| `findText(String, RangeElement)` | RangeElement | Continue search from position | Resume from previous result |
| `replaceText(String, String)` | Element | `ReplaceAllTextRequest` | Regex find and replace |
| `setText(String)` | Body | `DeleteContentRangeRequest` + `InsertTextRequest` | Clear and replace all content |
| `clear()` | Body | `DeleteContentRangeRequest` | Remove all content |

### Page & Margin Configuration

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getPageHeight()` | Number | `DocumentStyle.pageSize.height.magnitude` | In points |
| `setPageHeight(Number)` | Body | `UpdateDocumentStyleRequest` | Set page height |
| `getPageWidth()` | Number | `DocumentStyle.pageSize.width.magnitude` | In points |
| `setPageWidth(Number)` | Body | `UpdateDocumentStyleRequest` | Set page width |
| `getMarginTop()` | Number | `DocumentStyle.marginTop.magnitude` | In points |
| `setMarginTop(Number)` | Body | `UpdateDocumentStyleRequest` | Set top margin |
| `getMarginBottom()` | Number | `DocumentStyle.marginBottom.magnitude` | In points |
| `setMarginBottom(Number)` | Body | `UpdateDocumentStyleRequest` | Set bottom margin |
| `getMarginLeft()` | Number | `DocumentStyle.marginLeft.magnitude` | In points |
| `setMarginLeft(Number)` | Body | `UpdateDocumentStyleRequest` | Set left margin |
| `getMarginRight()` | Number | `DocumentStyle.marginRight.magnitude` | In points |
| `setMarginRight(Number)` | Body | `UpdateDocumentStyleRequest` | Set right margin |

### Attribute & Formatting Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getAttributes()` | Object | Extract from `DocumentStyle` | Get document-level attributes |
| `setAttributes(Object)` | Body | `UpdateDocumentStyleRequest` | Apply document attributes |
| `getHeadingAttributes(ParagraphHeading)` | Object | `DocumentStyle.namedStyles` + heading type filter | Get heading style definition |
| `setHeadingAttributes(ParagraphHeading, Object)` | Body | Update `DocumentStyle.namedStyles` | Modify heading style |
| `getTextAlignment()` | TextAlignment | `DocumentStyle.defaultHeaderId/FooterId` | Document text alignment |
| `setTextAlignment(TextAlignment)` | Body | `UpdateDocumentStyleRequest` | Set document alignment |

### Structure Navigation Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getParent()` | ContainerElement | Access parent `Tab` or `Document` | Navigate up tree |
| `getChildIndex(Element)` | Integer | Search `Body.content[]` for element | Find child position |
| `getType()` | ElementType | Check for `Body` class | Returns `BODY_SECTION` |
| `findElement(ElementType)` | RangeElement | Recursive search through tree | Find descendant by type |
| `findElement(ElementType, RangeElement)` | RangeElement | Continue search from position | Resume search |

### Element Manipulation Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `removeChild(Element)` | Body | `DeleteContentRangeRequest` | Remove child element |
| `copy()` | Body | Deep copy via `documents.get` + reconstruction | Detached clone |

---

## Paragraph

A block of text with consistent styling. Paragraphs may contain inline elements (text, images, page breaks, footnotes) but cannot contain newline characters (`\n` is converted to `\r`).

**REST API Equivalent**: The `Paragraph` resource (see [docs_api/03-structural-elements.md](../docs_api/03-structural-elements.md#paragraph)) within a `StructuralElement`.

### Content Creation Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `appendHorizontalRule()` | HorizontalRule | `InsertTextRequest` + style update | Append horizontal rule |
| `appendInlineImage(BlobSource)` | InlineImage | `InsertInlineImageRequest` at paragraph end | Embed image |
| `appendInlineImage(InlineImage)` | InlineImage | Clone existing image | Duplicate image |
| `appendPageBreak()` | PageBreak | `InsertPageBreakRequest` | Not allowed in table cells |
| `appendText(String)` | Text | `InsertTextRequest` | Append text content |
| `addPositionedImage(BlobSource)` | PositionedImage | Insert positioned object | Floating/anchored image |

### Content Insertion Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `insertHorizontalRule(Integer)` | HorizontalRule | `InsertTextRequest` + style | At child index |
| `insertInlineImage(Integer, BlobSource)` | InlineImage | `InsertInlineImageRequest` | At specific position |
| `insertInlineImage(Integer, InlineImage)` | InlineImage | Clone at position | Duplicate existing |
| `insertPageBreak(Integer)` | PageBreak | `InsertPageBreakRequest` | At child index |
| `insertText(Integer, String)` | Text | `InsertTextRequest` | At character position |

### Style Retrieval Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getAlignment()` | HorizontalAlignment | `ParagraphStyle.alignment` | LEFT, CENTER, RIGHT, JUSTIFIED |
| `getHeading()` | ParagraphHeading | `ParagraphStyle.namedStyleType` | NORMAL_TEXT, HEADING_1, etc. |
| `getIndentEnd()` | Number | `ParagraphStyle.indentEnd.magnitude` | In points |
| `getIndentFirstLine()` | Number | `ParagraphStyle.indentFirstLine.magnitude` | In points |
| `getIndentStart()` | Number | `ParagraphStyle.indentStart.magnitude` | In points |
| `getLineSpacing()` | Number | `ParagraphStyle.lineSpacing` | Multiplier (1 = single spacing) |
| `getSpacingAfter()` | Number | `ParagraphStyle.spaceAbove.magnitude` | In points |
| `getSpacingBefore()` | Number | `ParagraphStyle.spaceBelow.magnitude` | In points |
| `getTextAlignment()` | TextAlignment | Check if `ParagraphStyle` exists | Superscript/subscript state |
| `isLeftToRight()` | Boolean | `ParagraphStyle.direction` | LTR vs RTL text direction |

### Style Modification Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `setAlignment(HorizontalAlignment)` | Paragraph | `UpdateParagraphStyleRequest` | Set horizontal alignment |
| `setHeading(ParagraphHeading)` | Paragraph | `UpdateParagraphStyleRequest.namedStyleType` | Apply heading style |
| `setIndentEnd(Number)` | Paragraph | `UpdateParagraphStyleRequest.indentEnd` | Set end indentation |
| `setIndentFirstLine(Number)` | Paragraph | `UpdateParagraphStyleRequest.indentFirstLine` | Set first line indent |
| `setIndentStart(Number)` | Paragraph | `UpdateParagraphStyleRequest.indentStart` | Set start indentation |
| `setLineSpacing(Number)` | Paragraph | `UpdateParagraphStyleRequest.lineSpacing` | Set line spacing multiplier |
| `setSpacingAfter(Number)` | Paragraph | `UpdateParagraphStyleRequest.spaceBelow` | Set spacing after |
| `setSpacingBefore(Number)` | Paragraph | `UpdateParagraphStyleRequest.spaceAbove` | Set spacing before |
| `setTextAlignment(TextAlignment)` | Paragraph | `UpdateTextStyleRequest` | Superscript/subscript |
| `setLeftToRight(Boolean)` | Paragraph | `UpdateParagraphStyleRequest.direction` | Set text direction |
| `setLinkUrl(String)` | Paragraph | `UpdateTextStyleRequest.link` | Apply link to entire paragraph |

### Content Retrieval Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getText()` | String | Concatenate all `textRun.content` | Get paragraph text |
| `getAttributes()` | Object | Extract `ParagraphStyle` fields | Get all attributes |
| `getLinkUrl()` | String | Check `TextStyle.link.url` | Get paragraph link |
| `getPositionedImage(String)` | PositionedImage | Lookup in `positionedObjectIds[]` | Get anchored image by ID |
| `getPositionedImages()` | PositionedImage[] | Retrieve all `positionedObjectIds[]` | Get all anchored images |

### Navigation Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getChild(Integer)` | Element | Access `Paragraph.elements[]` | Get child element |
| `getNumChildren()` | Integer | `Paragraph.elements.length` | Count inline elements |
| `getParent()` | ContainerElement | Navigate up to `Body` or `TableCell` | Get parent container |
| `getNextSibling()` | Element | Find next in `Body.content[]` | Next structural element |
| `getPreviousSibling()` | Element | Find previous in `Body.content[]` | Previous element |
| `getType()` | ElementType | Check element class | Returns `PARAGRAPH` |
| `isAtDocumentEnd()` | Boolean | Check if last element in `Body.content[]` | At document end |

### Text Operations Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `editAsText()` | Text | Convert to text interface | Character-level editing |
| `findText(String)` | RangeElement | Search `textRun.content` fields | Regex search |
| `findText(String, RangeElement)` | RangeElement | Continue from position | Resume search |
| `replaceText(String, String)` | Element | `ReplaceAllTextRequest` | Regex replacement |
| `setText(String)` | void | `DeleteContentRangeRequest` + `InsertTextRequest` | Replace paragraph content |
| `findElement(ElementType)` | RangeElement | Search `Paragraph.elements[]` | Find child by type |
| `findElement(ElementType, RangeElement)` | RangeElement | Continue search | Resume from position |

### Structural Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `clear()` | Paragraph | `DeleteContentRangeRequest` | Remove all content |
| `copy()` | Paragraph | Deep copy via reconstruction | Detached clone |
| `merge()` | Paragraph | Merge with previous sibling | Combines paragraphs |
| `removeChild(Element)` | Paragraph | `DeleteContentRangeRequest` | Remove child element |
| `removeFromParent()` | Paragraph | Remove from `Body.content[]` | Detach from parent |
| `removePositionedImage(String)` | Boolean | `DeletePositionedObjectRequest` | Remove anchored image |
| `setAttributes(Object)` | Paragraph | `UpdateParagraphStyleRequest` | Apply multiple attributes |

---

## ListItem

A paragraph associated with a list, extending `Paragraph` with list-specific formatting methods. ListItems cannot contain newline characters.

**REST API Equivalent**: A `Paragraph` resource with a `bullet` field containing `listId` and `nestingLevel` (see [docs_api/07-lists-named-ranges.md](../docs_api/07-lists-named-ranges.md#bullet)).

### Inherited Methods

ListItem inherits all methods from Paragraph (see above) plus the following list-specific methods:

### List-Specific Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getGlyphType()` | GlyphType | `List.nestingLevels[level].glyphType` | Bullet style at nesting level |
| `setGlyphType(GlyphType)` | ListItem | Update `List.nestingLevels[level].glyphType` | Change bullet style |
| `getListId()` | String | `Paragraph.bullet.listId` | List identifier |
| `setListId(ListItem)` | ListItem | Copy `bullet.listId` from another item | Join same list |
| `getNestingLevel()` | Integer | `Paragraph.bullet.nestingLevel` | Current indent depth (0-8) |
| `setNestingLevel(Integer)` | ListItem | `UpdateParagraphStyleRequest` + update `bullet.nestingLevel` | Change list depth |

### Key Difference from REST API

Apps Script abstracts list management through `ListItem` methods. REST API requires:
1. Ensuring a list ID exists (or creating one via `CreateParagraphBulletsRequest`)
2. Updating paragraph's `bullet` field with `listId` and `nestingLevel`
3. Maintaining `List.nestingLevels[]` configuration separately

Apps Script's `setGlyphType()` automatically manages the list configuration, while REST API requires explicit `List.nestingLevels[]` updates.

---

## Table

A tabular data structure containing only `TableRow` elements. Google Docs documents cannot end with a table, so Apps Script automatically appends an empty paragraph after table creation.

**REST API Equivalent**: The `Table` resource (see [docs_api/03-structural-elements.md](../docs_api/03-structural-elements.md#table)) within a `StructuralElement`.

### Row Creation Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `appendTableRow()` | TableRow | `InsertTableRowRequest` | Add empty row at end |
| `appendTableRow(TableRow)` | TableRow | `InsertTableRowRequest` + clone cells | Clone and append row |
| `insertTableRow(Integer)` | TableRow | `InsertTableRowRequest` | Insert empty row at index |

### Table Style Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getBorderColor()` | String | `TableStyle.borderColor` | CSS notation (e.g., "#ff0000") |
| `setBorderColor(String)` | Table | Update `TableStyle.borderColor` | Set border color |
| `getBorderWidth()` | Number | `TableStyle.borderWidth.magnitude` | In points |
| `setBorderWidth(Number)` | Table | Update `TableStyle.borderWidth` | Set border thickness |
| `getColumnWidth(Integer)` | Number | `TableColumnProperties[index].width.magnitude` | Column width in points |
| `setColumnWidth(Integer, Number)` | Table | `UpdateTableColumnPropertiesRequest` | Set specific column width |

### Content Access Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getRow(Integer)` | TableRow | Access `Table.tableRows[]` | Get row by index |
| `getCell(Integer, Integer)` | TableCell | Access `Table.tableRows[row].tableCells[col]` | Get cell by coordinates |
| `getNumRows()` | Integer | `Table.rows` | Count rows |

### Navigation & Search Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getText()` | String | Concatenate all cell text | Get table text content |
| `editAsText()` | Text | Convert to text interface | Character-level operations |
| `findText(String)` | RangeElement | Search all cell `textRun.content` | Regex search |
| `findElement(ElementType)` | RangeElement | Recursive search through rows/cells | Find descendant by type |

### Structural Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `removeRow(Integer)` | TableRow | `DeleteTableRowRequest` | Delete row at index |
| `clear()` | Table | `DeleteContentRangeRequest` for all cells | Remove all content |
| `copy()` | Table | Deep copy via reconstruction | Detached clone |
| `getAttributes()` | Object | Extract `TableStyle` fields | Get table attributes |

---

## TableRow

A row within a table, containing only `TableCell` elements. Always contained within a `Table`.

**REST API Equivalent**: The `TableRow` resource (see [docs_api/03-structural-elements.md](../docs_api/03-structural-elements.md#tablerow)).

### Cell Creation Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `appendTableCell()` | TableCell | `InsertTableColumnRequest` | Add empty cell at end |
| `appendTableCell(String)` | TableCell | `InsertTableColumnRequest` + `InsertTextRequest` | Cell with text content |
| `appendTableCell(TableCell)` | TableCell | Clone cell structure | Duplicate existing cell |
| `insertTableCell(Integer)` | TableCell | `InsertTableColumnRequest` | Insert empty cell at index |
| `insertTableCell(Integer, String)` | TableCell | Insert + populate | Cell with text at position |
| `insertTableCell(Integer, TableCell)` | TableCell | Clone at position | Duplicate at index |

### Row Style Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getMinimumHeight()` | Number | `TableRowStyle.minRowHeight.magnitude` | In points |
| `setMinimumHeight(Number)` | TableRow | `UpdateTableRowStyleRequest` | Set minimum row height |

### Content Access Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getCell(Integer)` | TableCell | Access `TableRow.tableCells[]` | Get cell by index |
| `getNumCells()` | Integer | `TableRow.tableCells.length` | Count cells in row |
| `getText()` | String | Concatenate cell text | Get row text content |
| `getTextAlignment()` | TextAlignment | Check cell `TextStyle` | Row text alignment |
| `setTextAlignment(TextAlignment)` | TableRow | `UpdateTextStyleRequest` across cells | Apply to all cells |

### Navigation Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getChild(Integer)` | Element | Access `tableCells[]` | Get child element |
| `getChildIndex(Element)` | Integer | Search `tableCells[]` | Find cell index |
| `getNumChildren()` | Integer | `tableCells.length` | Count child elements |
| `getParent()` | ContainerElement | Navigate to `Table` | Get parent table |
| `getParentTable()` | Table | Direct parent access | Get containing table |
| `getNextSibling()` | Element | Next in `Table.tableRows[]` | Next row |
| `getPreviousSibling()` | Element | Previous in `Table.tableRows[]` | Previous row |
| `getType()` | ElementType | Check element class | Returns `TABLE_ROW` |
| `isAtDocumentEnd()` | Boolean | Check if last row | At document end |

### Text Operations Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `editAsText()` | Text | Convert to text interface | Character-level editing |
| `findText(String)` | RangeElement | Search cell `textRun.content` | Regex search |
| `findElement(ElementType)` | RangeElement | Search through cells | Find descendant by type |
| `replaceText(String, String)` | Element | `ReplaceAllTextRequest` | Regex replacement |

### Structural Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `removeCell(Integer)` | TableCell | `DeleteTableColumnRequest` | Remove cell at index |
| `clear()` | TableRow | `DeleteContentRangeRequest` for cells | Remove all content |
| `copy()` | TableRow | Deep copy via reconstruction | Detached clone |
| `merge()` | TableRow | Merge with previous sibling | Combines rows |
| `removeChild(Element)` | TableRow | Remove cell | Delete child element |
| `removeFromParent()` | TableRow | Remove from table | Detach from parent |
| `getAttributes()` | Object | Extract `TableRowStyle` | Get row attributes |
| `setAttributes(Object)` | TableRow | `UpdateTableRowStyleRequest` | Apply attributes |
| `getLinkUrl()` | String | Check cell `TextStyle.link` | Get row link |
| `setLinkUrl(String)` | TableRow | Apply link to all cells | Set link on row |

---

## TableCell

A cell within a table row. May contain `Paragraph`, `ListItem`, or nested `Table` elements. Always contained within a `TableRow`.

**REST API Equivalent**: The `TableCell` resource (see [docs_api/03-structural-elements.md](../docs_api/03-structural-elements.md#tablecell)).

### Content Creation Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `appendHorizontalRule()` | HorizontalRule | `InsertTextRequest` + style | Append horizontal rule |
| `appendImage(BlobSource)` | InlineImage | `InsertInlineImageRequest` | Embed image from blob |
| `appendImage(InlineImage)` | InlineImage | Clone existing image | Duplicate image |
| `appendListItem(String)` | ListItem | `InsertTextRequest` + `CreateParagraphBulletsRequest` | Create list item |
| `appendListItem(ListItem)` | ListItem | Clone list item structure | Duplicate item |
| `appendParagraph(String)` | Paragraph | `InsertTextRequest` | Add text paragraph |
| `appendParagraph(Paragraph)` | Paragraph | Clone paragraph | Duplicate paragraph |
| `appendTable()` | Table | `InsertTableRequest` | Nested empty table |
| `appendTable(String[][])` | Table | `InsertTableRequest` + populate | Nested table with data |
| `appendTable(Table)` | Table | Clone table structure | Duplicate nested table |

### Content Insertion Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `insertHorizontalRule(Integer)` | HorizontalRule | `InsertTextRequest` + style | At child index |
| `insertImage(Integer, BlobSource)` | InlineImage | `InsertInlineImageRequest` | At specific position |
| `insertImage(Integer, InlineImage)` | InlineImage | Clone at position | Duplicate at index |
| `insertListItem(Integer, String)` | ListItem | Insert + convert to list | At position |
| `insertListItem(Integer, ListItem)` | ListItem | Clone at position | Duplicate at index |
| `insertParagraph(Integer, String)` | Paragraph | `InsertTextRequest` | At child index |
| `insertParagraph(Integer, Paragraph)` | Paragraph | Clone at position | Duplicate at index |
| `insertTable(Integer)` | Table | `InsertTableRequest` | Nested table at index |
| `insertTable(Integer, String[][])` | Table | Insert + populate | With data at position |
| `insertTable(Integer, Table)` | Table | Clone at position | Duplicate at index |

### Cell Style Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getBackgroundColor()` | String | `TableCellStyle.backgroundColor.color` | CSS hex notation |
| `setBackgroundColor(String)` | TableCell | `UpdateTableCellStyleRequest` | Set cell background |
| `getPaddingBottom()` | Number | `TableCellStyle.paddingBottom.magnitude` | In points |
| `setPaddingBottom(Number)` | TableCell | `UpdateTableCellStyleRequest.paddingBottom` | Set bottom padding |
| `getPaddingLeft()` | Number | `TableCellStyle.paddingLeft.magnitude` | In points |
| `setPaddingLeft(Number)` | TableCell | `UpdateTableCellStyleRequest.paddingLeft` | Set left padding |
| `getPaddingRight()` | Number | `TableCellStyle.paddingRight.magnitude` | In points |
| `setPaddingRight(Number)` | TableCell | `UpdateTableCellStyleRequest.paddingRight` | Set right padding |
| `getPaddingTop()` | Number | `TableCellStyle.paddingTop.magnitude` | In points |
| `setPaddingTop(Number)` | TableCell | `UpdateTableCellStyleRequest.paddingTop` | Set top padding |
| `getWidth()` | Number | Column width from `TableColumnProperties` | In points |
| `setWidth(Number)` | TableCell | `UpdateTableColumnPropertiesRequest` | Set cell width |

### Cell Properties Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getColSpan()` | Integer | `TableCellStyle.columnSpan` | Columns merged |
| `getRowSpan()` | Integer | `TableCellStyle.rowSpan` | Rows merged |
| `getVerticalAlignment()` | VerticalAlignment | `TableCellStyle.contentAlignment` | TOP, MIDDLE, BOTTOM |
| `setVerticalAlignment(VerticalAlignment)` | TableCell | `UpdateTableCellStyleRequest.contentAlignment` | Set vertical alignment |
| `getTextAlignment()` | TextAlignment | Check paragraph `TextStyle` | Superscript/subscript |
| `setTextAlignment(TextAlignment)` | TableCell | `UpdateTextStyleRequest` across content | Apply to cell text |

### Content Access Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getText()` | String | Concatenate `textRun.content` | Get cell text content |
| `setText(String)` | TableCell | `DeleteContentRangeRequest` + `InsertTextRequest` | Replace cell content |
| `getChild(Integer)` | Element | Access `TableCell.content[]` | Get child element |
| `getChildIndex(Element)` | Integer | Search `content[]` | Find element index |
| `getNumChildren()` | Integer | `content.length` | Count child elements |

### Navigation Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `getParent()` | ContainerElement | Navigate to `TableRow` | Get parent row |
| `getParentRow()` | TableRow | Direct parent access | Get containing row |
| `getParentTable()` | Table | Navigate up two levels | Get containing table |
| `getNextSibling()` | Element | Next in `TableRow.tableCells[]` | Next cell |
| `getPreviousSibling()` | Element | Previous in `tableCells[]` | Previous cell |
| `getType()` | ElementType | Check element class | Returns `TABLE_CELL` |
| `isAtDocumentEnd()` | Boolean | Check if last cell in last row | At document end |

### Text Operations Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `editAsText()` | Text | Convert to text interface | Character-level editing |
| `findText(String)` | RangeElement | Search `textRun.content` | Regex search |
| `findElement(ElementType)` | RangeElement | Search through content | Find descendant by type |
| `replaceText(String, String)` | Element | `ReplaceAllTextRequest` | Regex replacement |

### Structural Methods

| Method | Return Type | REST API Equivalent | Notes |
|--------|-------------|---------------------|-------|
| `clear()` | TableCell | `DeleteContentRangeRequest` | Remove all content |
| `copy()` | TableCell | Deep copy via reconstruction | Detached clone |
| `merge()` | TableCell | `MergeTableCellsRequest` | Merge with adjacent cells |
| `removeChild(Element)` | TableCell | Remove element | Delete child |
| `removeFromParent()` | TableCell | Remove cell | Detach from row |
| `getAttributes()` | Object | Extract `TableCellStyle` | Get cell attributes |
| `setAttributes(Object)` | TableCell | `UpdateTableCellStyleRequest` | Apply attributes |
| `getLinkUrl()` | String | Check `TextStyle.link` | Get cell link |
| `setLinkUrl(String)` | TableCell | Apply link to all content | Set link on cell |

---

## Coverage Summary

### Total Method Count by Class

| Class | Total Methods | Apps Script Only | REST API Equivalent |
|-------|--------------|------------------|---------------------|
| **Body** | 48 | 0 | 48 |
| **Paragraph** | 51 | 0 | 51 |
| **ListItem** | 57 (51 inherited + 6 list-specific) | 0 | 57 |
| **Table** | 17 | 0 | 17 |
| **TableRow** | 39 | 0 | 39 |
| **TableCell** | 64 | 0 | 64 |
| **Total** | **276** | **0** | **276** |

### Key Observations

1. **Full REST API Coverage**: Every Apps Script structural element method has a REST API equivalent through `batchUpdate` request types.

2. **Convenience vs. Composition**: Apps Script provides high-level convenience methods (e.g., `appendParagraph(String)`) that map to multiple REST API operations (`InsertTextRequest` + potential style updates).

3. **Tree vs. Index Navigation**: Apps Script's DOM-like navigation (`getChild`, `getParent`, `getNextSibling`) requires manual index tracking in REST API's flat `content[]` arrays.

4. **Immediate vs. Batched Execution**: Apps Script methods execute immediately, while REST API requires bundling changes into `batchUpdate` requests.

5. **List Abstraction**: Apps Script's `ListItem` class hides the complexity of REST API's separate `List` resource + `Paragraph.bullet` coordination.

6. **Style Management**: Apps Script's attribute getters/setters map to REST API's `Update*StyleRequest` types with explicit `fields` masks for partial updates.

### Apps Script Advantages

- **Intuitive navigation**: Tree-based traversal feels natural for document manipulation
- **Fewer calls**: Single method combines multiple REST API operations
- **Automatic management**: List and style inheritance handled implicitly
- **Type safety**: Strong typing via class methods vs. union field selection

### REST API Advantages

- **Batch efficiency**: Multiple changes in single network request
- **Granular control**: Explicit field masks for partial updates
- **Language agnostic**: JSON requests work from any environment
- **Concurrent safety**: Read document state once, apply batch without re-reading

---

## Migration Patterns

### Apps Script → REST API

**Pattern 1: Tree navigation → Index tracking**
```javascript
// Apps Script
const cell = body.getChild(5).asTable().getRow(2).getCell(1);

// REST API: Must track indices manually
const table = body.content[5].table;
const row = table.tableRows[2];
const cell = row.tableCells[1];
```

**Pattern 2: Convenience methods → Composed requests**
```javascript
// Apps Script
body.appendParagraph("Hello World");

// REST API: Two operations
batchUpdate([
  { insertText: { text: "Hello World\n", endOfSegmentLocation: { segmentId: "" } } }
]);
```

**Pattern 3: List management → Manual coordination**
```javascript
// Apps Script
listItem.setGlyphType(DocumentApp.GlyphType.BULLET);
listItem.setNestingLevel(1);

// REST API: Update paragraph bullet + list definition
batchUpdate([
  { updateParagraphStyle: {
      range: { startIndex: X, endIndex: Y },
      paragraphStyle: { bullet: { listId: "kix.xyz", nestingLevel: 1 } },
      fields: "bullet"
    }
  }
]);
```

### REST API → Apps Script

**Pattern 1: Batch requests → Sequential method calls**
```javascript
// REST API
batchUpdate([
  { insertText: { ... } },
  { updateTextStyle: { ... } },
  { createParagraphBullets: { ... } }
]);

// Apps Script
body.appendListItem("Hello");
listItem.setGlyphType(DocumentApp.GlyphType.BULLET);
```

**Pattern 2: Index ranges → Element references**
```javascript
// REST API
updateTextStyle({ range: { startIndex: 100, endIndex: 150 }, ... });

// Apps Script
const paragraph = body.getParagraphs()[5];
paragraph.editAsText().setBold(0, 50, true);
```

**Pattern 3: Field masks → Setter methods**
```javascript
// REST API
updateParagraphStyle({
  paragraphStyle: { alignment: "CENTER", lineSpacing: 1.5 },
  fields: "alignment,lineSpacing"
});

// Apps Script
paragraph.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
paragraph.setLineSpacing(1.5);
```
