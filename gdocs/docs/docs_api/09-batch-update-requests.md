# BatchUpdate Request Types

All 37 request types for `documents.batchUpdate`. Each request is a union field — exactly one type per request object.

## Text Operations

### InsertTextRequest

Inserts text at a specified location.

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | The text to insert. |
| `location` | [`Location`](./12-common-types.md#location) | Specific index insertion point. |
| `endOfSegmentLocation` | [`EndOfSegmentLocation`](./12-common-types.md#endofsegmentlocation) | Insert at end of header/footer/footnote/body. |

### DeleteContentRangeRequest

Deletes content within a range.

| Field | Type | Description |
|-------|------|-------------|
| `range` | [`Range`](./12-common-types.md#range) | The range of content to delete. |

### ReplaceAllTextRequest

Replaces all instances of matching text across the document.

| Field | Type | Description |
|-------|------|-------------|
| `containsText` | [`SubstringMatchCriteria`](./12-common-types.md#substringmatchcriteria) | Search criteria. |
| `replaceText` | string | Replacement text. |
| `tabsCriteria` | [`TabsCriteria`](./08-tabs.md#tabscriteria) | Optional tab filter. |

### ReplaceNamedRangeContentRequest

Replaces content within a named range.

| Field | Type | Description |
|-------|------|-------------|
| `namedRangeId` | string | ID of the named range. |
| `namedRangeName` | string | Name of the named range(s). |
| `text` | string | Replacement content. |
| `tabsCriteria` | [`TabsCriteria`](./08-tabs.md#tabscriteria) | Optional tab filter. |

---

## Style Operations

### UpdateTextStyleRequest

Modifies character-level formatting on a text range.

| Field | Type | Description |
|-------|------|-------------|
| `textStyle` | [`TextStyle`](./05-styles.md#textstyle) | Styling to apply. |
| `fields` | string (FieldMask) | Which `TextStyle` fields to update. |
| `range` | [`Range`](./12-common-types.md#range) | Text range to style. |

### UpdateParagraphStyleRequest

Modifies paragraph-level formatting.

| Field | Type | Description |
|-------|------|-------------|
| `paragraphStyle` | [`ParagraphStyle`](./05-styles.md#paragraphstyle) | Styles to apply. |
| `fields` | string (FieldMask) | Which fields to update. |
| `range` | [`Range`](./12-common-types.md#range) | Paragraphs to style. |

### UpdateDocumentStyleRequest

Changes document-wide style settings.

| Field | Type | Description |
|-------|------|-------------|
| `documentStyle` | [`DocumentStyle`](./05-styles.md#documentstyle) | Styles to apply. |
| `fields` | string (FieldMask) | Which fields to update. |
| `tabId` | string | Optional tab identifier. |

### UpdateSectionStyleRequest

Modifies section-level formatting.

| Field | Type | Description |
|-------|------|-------------|
| `range` | [`Range`](./12-common-types.md#range) | Section range. |
| `sectionStyle` | [`SectionStyle`](./05-styles.md#sectionstyle) | Style properties. |
| `fields` | string (FieldMask) | Which fields to update. |

---

## List Operations

### CreateParagraphBulletsRequest

Converts paragraphs into bulleted/numbered lists.

| Field | Type | Description |
|-------|------|-------------|
| `range` | [`Range`](./12-common-types.md#range) | Range of paragraphs. |
| `bulletPreset` | enum [`BulletGlyphPreset`](./11-enums.md#bulletglyphpreset) | Bullet style preset. |

### DeleteParagraphBulletsRequest

Removes bullet formatting from paragraphs.

| Field | Type | Description |
|-------|------|-------------|
| `range` | [`Range`](./12-common-types.md#range) | Range to remove bullets from. |

---

## Named Range Operations

### CreateNamedRangeRequest

Creates a labeled range for programmatic reference.

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Range name (1–256 UTF-16 code units). |
| `range` | [`Range`](./12-common-types.md#range) | Range to name. |

### DeleteNamedRangeRequest

Removes a named range.

| Field | Type | Description |
|-------|------|-------------|
| `namedRangeId` | string | ID of range to delete. |
| `name` | string | Name of range(s) to delete. |
| `tabsCriteria` | [`TabsCriteria`](./08-tabs.md#tabscriteria) | Optional tab filter. |

---

## Table Operations

### InsertTableRequest

Creates a new table.

| Field | Type | Description |
|-------|------|-------------|
| `rows` | integer | Number of rows. |
| `columns` | integer | Number of columns. |
| `location` | [`Location`](./12-common-types.md#location) | Specific index. |
| `endOfSegmentLocation` | [`EndOfSegmentLocation`](./12-common-types.md#endofsegmentlocation) | End of segment. |

### InsertTableRowRequest

Adds a row to an existing table.

| Field | Type | Description |
|-------|------|-------------|
| `tableCellLocation` | [`TableCellLocation`](./12-common-types.md#tablecelllocation) | Reference cell. |
| `insertBelow` | boolean | `true` = below, `false` = above. |

### InsertTableColumnRequest

Adds a column to an existing table.

| Field | Type | Description |
|-------|------|-------------|
| `tableCellLocation` | [`TableCellLocation`](./12-common-types.md#tablecelllocation) | Reference cell. |
| `insertRight` | boolean | `true` = right, `false` = left. |

### DeleteTableRowRequest

Removes a table row.

| Field | Type | Description |
|-------|------|-------------|
| `tableCellLocation` | [`TableCellLocation`](./12-common-types.md#tablecelllocation) | Cell in the row to delete. |

### DeleteTableColumnRequest

Removes a table column.

| Field | Type | Description |
|-------|------|-------------|
| `tableCellLocation` | [`TableCellLocation`](./12-common-types.md#tablecelllocation) | Cell in the column to delete. |

### MergeTableCellsRequest

Combines adjacent table cells.

| Field | Type | Description |
|-------|------|-------------|
| `tableRange` | [`TableRange`](./12-common-types.md#tablerange) | Range of cells to merge. |

### UnmergeTableCellsRequest

Separates previously merged cells.

| Field | Type | Description |
|-------|------|-------------|
| `tableRange` | [`TableRange`](./12-common-types.md#tablerange) | Range of cells to unmerge. |

### UpdateTableColumnPropertiesRequest

Modifies column width and formatting.

| Field | Type | Description |
|-------|------|-------------|
| `tableStartLocation` | [`Location`](./12-common-types.md#location) | Table start position. |
| `columnIndices[]` | integer | Columns to update (0-indexed). |
| `tableColumnProperties` | [`TableColumnProperties`](./05-styles.md#tablecolumnproperties) | Properties to set. |
| `fields` | string (FieldMask) | Which fields to update. |

### UpdateTableCellStyleRequest

Modifies cell styling.

| Field | Type | Description |
|-------|------|-------------|
| `tableCellStyle` | [`TableCellStyle`](./05-styles.md#tablecellstyle) | Style properties. |
| `fields` | string (FieldMask) | Which fields to update. |
| `tableRange` | [`TableRange`](./12-common-types.md#tablerange) | Cell range. |
| `tableStartLocation` | [`Location`](./12-common-types.md#location) | Table location. |

### UpdateTableRowStyleRequest

Modifies row height and properties.

| Field | Type | Description |
|-------|------|-------------|
| `tableStartLocation` | [`Location`](./12-common-types.md#location) | Table position. |
| `rowIndices[]` | integer | Rows to update (0-indexed). |
| `tableRowStyle` | [`TableRowStyle`](./05-styles.md#tablerowstyle) | Style properties. |
| `fields` | string (FieldMask) | Which fields to update. |

### PinTableHeaderRowsRequest

Pins header rows so they repeat across pages.

| Field | Type | Description |
|-------|------|-------------|
| `tableStartLocation` | [`Location`](./12-common-types.md#location) | Table position. |
| `pinnedHeaderRowsCount` | integer | Number of rows to pin. |

---

## Image Operations

### InsertInlineImageRequest

Embeds an image inline with text.

| Field | Type | Description |
|-------|------|-------------|
| `uri` | string | Publicly accessible image URI (max 2KB URL length). |
| `objectSize` | [`Size`](./06-objects.md#size) | Optional dimensions. |
| `location` | [`Location`](./12-common-types.md#location) | Specific index. |
| `endOfSegmentLocation` | [`EndOfSegmentLocation`](./12-common-types.md#endofsegmentlocation) | End of segment. |

### ReplaceImageRequest

Replaces an existing image with a new one.

| Field | Type | Description |
|-------|------|-------------|
| `imageObjectId` | string | ID of the image to replace. |
| `uri` | string | New image URI. |
| `imageReplaceMethod` | enum [`ImageReplaceMethod`](./11-enums.md#imagereplacemethod) | Replacement method. |
| `tabId` | string | Optional tab identifier. |

### DeletePositionedObjectRequest

Removes a positioned (floating) object.

| Field | Type | Description |
|-------|------|-------------|
| `objectId` | string | Object identifier. |
| `tabId` | string | Optional tab identifier. |

---

## Structural Operations

### InsertPageBreakRequest

Inserts a page break.

| Field | Type | Description |
|-------|------|-------------|
| `location` | [`Location`](./12-common-types.md#location) | Specific index. |
| `endOfSegmentLocation` | [`EndOfSegmentLocation`](./12-common-types.md#endofsegmentlocation) | End of body. |

### InsertSectionBreakRequest

Creates a new section with independent formatting.

| Field | Type | Description |
|-------|------|-------------|
| `sectionType` | enum [`SectionType`](./11-enums.md#sectiontype) | Break type. |
| `location` | [`Location`](./12-common-types.md#location) | Specific index. |
| `endOfSegmentLocation` | [`EndOfSegmentLocation`](./12-common-types.md#endofsegmentlocation) | End of body. |

---

## Header/Footer/Footnote Operations

### CreateHeaderRequest

Adds a header to a document section.

| Field | Type | Description |
|-------|------|-------------|
| `type` | enum [`HeaderFooterType`](./11-enums.md#headerfootertype) | Header type (DEFAULT). |
| `sectionBreakLocation` | [`Location`](./12-common-types.md#location) | Optional section location. |

### CreateFooterRequest

Adds a footer to a document section.

| Field | Type | Description |
|-------|------|-------------|
| `type` | enum [`HeaderFooterType`](./11-enums.md#headerfootertype) | Footer type (DEFAULT). |
| `sectionBreakLocation` | [`Location`](./12-common-types.md#location) | Optional section location. |

### CreateFootnoteRequest

Inserts a footnote with automatic numbering.

| Field | Type | Description |
|-------|------|-------------|
| `location` | [`Location`](./12-common-types.md#location) | Specific index. |
| `endOfSegmentLocation` | [`EndOfSegmentLocation`](./12-common-types.md#endofsegmentlocation) | End of body. |

### DeleteHeaderRequest

Removes a header.

| Field | Type | Description |
|-------|------|-------------|
| `headerId` | string | Header identifier. |
| `tabId` | string | Optional tab identifier. |

### DeleteFooterRequest

Removes a footer.

| Field | Type | Description |
|-------|------|-------------|
| `footerId` | string | Footer identifier. |
| `tabId` | string | Optional tab identifier. |

---

## Tab Operations

### AddDocumentTabRequest

Creates a new document tab.

| Field | Type | Description |
|-------|------|-------------|
| `tabProperties` | [`TabProperties`](./08-tabs.md#tabproperties) | Tab configuration. |

### DeleteTabRequest

Removes a document tab.

| Field | Type | Description |
|-------|------|-------------|
| `tabId` | string | Tab identifier. |

### UpdateDocumentTabPropertiesRequest

Modifies tab settings.

| Field | Type | Description |
|-------|------|-------------|
| `tabProperties` | [`TabProperties`](./08-tabs.md#tabproperties) | Properties to update. |
| `fields` | string (FieldMask) | Which fields to update. |

---

## Person Operations

### InsertPersonRequest

Adds a person mention (@-mention) smart chip.

| Field | Type | Description |
|-------|------|-------------|
| `personProperties` | [`PersonProperties`](./04-paragraph-elements.md#personproperties) | Person details (name, email). |
| `location` | [`Location`](./12-common-types.md#location) | Specific index. |
| `endOfSegmentLocation` | [`EndOfSegmentLocation`](./12-common-types.md#endofsegmentlocation) | End of segment. |
