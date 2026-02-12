# Text and Inline Elements

Apps Script classes for text manipulation and inline elements (images, drawings, horizontal rules, page breaks).

---

## Text

Represents a rich text region within a document. All document text is contained within Text elements.

### Characteristics

- Cannot contain other elements (leaf node)
- Can be contained within Equation, EquationFunction, ListItem, or Paragraph
- Supports comprehensive character-level formatting

### Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| **Text Content** |
| `getText()` | String | Retrieves text content | Read `TextRun.content` |
| `setText(text)` | Text | Replaces entire content | `batchUpdate`: DeleteContentRangeRequest + InsertTextRequest |
| `appendText(text)` | Text | Adds text to end | `batchUpdate`: InsertTextRequest |
| `insertText(offset, text)` | Text | Inserts at position | `batchUpdate`: InsertTextRequest with `location.index` |
| `deleteText(startOffset, endOffsetInclusive)` | Text | Removes text range | `batchUpdate`: DeleteContentRangeRequest |
| **Bold/Italic/Underline/Strikethrough** |
| `isBold()` | Boolean | Gets bold state | Read `TextRun.textStyle.bold` |
| `setBold(bold)` | Text | Sets bold for entire text | `batchUpdate`: UpdateTextStyleRequest |
| `isBold(offset)` | Boolean | Gets bold at offset | Read `TextRun.textStyle.bold` at position |
| `setBold(startOffset, endOffsetInclusive, bold)` | Text | Sets bold for range | `batchUpdate`: UpdateTextStyleRequest with range |
| `isItalic()` | Boolean | Gets italic state | Read `TextRun.textStyle.italic` |
| `setItalic(italic)` | Text | Sets italic | `batchUpdate`: UpdateTextStyleRequest |
| `isItalic(offset)` | Boolean | Gets italic at offset | Read `TextRun.textStyle.italic` at position |
| `setItalic(startOffset, endOffsetInclusive, italic)` | Text | Sets italic for range | `batchUpdate`: UpdateTextStyleRequest with range |
| `isUnderline()` | Boolean | Gets underline state | Read `TextRun.textStyle.underline` |
| `setUnderline(underline)` | Text | Sets underline | `batchUpdate`: UpdateTextStyleRequest |
| `isUnderline(offset)` | Boolean | Gets underline at offset | Read `TextRun.textStyle.underline` at position |
| `setUnderline(startOffset, endOffsetInclusive, underline)` | Text | Sets underline for range | `batchUpdate`: UpdateTextStyleRequest with range |
| `isStrikethrough()` | Boolean | Gets strikethrough state | Read `TextRun.textStyle.strikethrough` |
| `setStrikethrough(strikethrough)` | Text | Sets strikethrough | `batchUpdate`: UpdateTextStyleRequest |
| `isStrikethrough(offset)` | Boolean | Gets strikethrough at offset | Read `TextRun.textStyle.strikethrough` at position |
| `setStrikethrough(startOffset, endOffsetInclusive, strikethrough)` | Text | Sets strikethrough for range | `batchUpdate`: UpdateTextStyleRequest with range |
| **Colors** |
| `getForegroundColor()` | String (hex) | Gets text color | Read `TextRun.textStyle.foregroundColor.color.rgbColor` |
| `setForegroundColor(color)` | Text | Sets text color | `batchUpdate`: UpdateTextStyleRequest with `foregroundColor` |
| `getForegroundColor(offset)` | String | Gets color at offset | Read `TextRun.textStyle.foregroundColor` at position |
| `setForegroundColor(startOffset, endOffsetInclusive, color)` | Text | Sets color for range | `batchUpdate`: UpdateTextStyleRequest with range |
| `getBackgroundColor()` | String | Gets background color | Read `TextRun.textStyle.backgroundColor.color.rgbColor` |
| `setBackgroundColor(color)` | Text | Sets background | `batchUpdate`: UpdateTextStyleRequest with `backgroundColor` |
| `getBackgroundColor(offset)` | String | Gets background at offset | Read `TextRun.textStyle.backgroundColor` at position |
| `setBackgroundColor(startOffset, endOffsetInclusive, color)` | Text | Sets background for range | `batchUpdate`: UpdateTextStyleRequest with range |
| **Font** |
| `getFontFamily()` | String | Gets font family | Read `TextRun.textStyle.weightedFontFamily.fontFamily` |
| `setFontFamily(fontFamily)` | Text | Sets font | `batchUpdate`: UpdateTextStyleRequest with `weightedFontFamily` |
| `getFontFamily(offset)` | String | Gets font at offset | Read `TextRun.textStyle.weightedFontFamily` at position |
| `setFontFamily(startOffset, endOffsetInclusive, fontFamily)` | Text | Sets font for range | `batchUpdate`: UpdateTextStyleRequest with range |
| `getFontSize()` | Number | Gets font size | Read `TextRun.textStyle.fontSize.magnitude` |
| `setFontSize(size)` | Text | Sets font size | `batchUpdate`: UpdateTextStyleRequest with `fontSize` |
| `getFontSize(offset)` | Number | Gets font size at offset | Read `TextRun.textStyle.fontSize` at position |
| `setFontSize(startOffset, endOffsetInclusive, size)` | Text | Sets font size for range | `batchUpdate`: UpdateTextStyleRequest with range |
| **Alignment & Links** |
| `getTextAlignment()` | TextAlignment | Gets alignment | Read `Paragraph.paragraphStyle.alignment` |
| `setTextAlignment(alignment)` | Text | Sets alignment | `batchUpdate`: UpdateParagraphStyleRequest |
| `getTextAlignment(offset)` | TextAlignment | Gets alignment at offset | Read `Paragraph.paragraphStyle.alignment` |
| `setTextAlignment(startOffset, endOffsetInclusive, alignment)` | Text | Sets alignment for range | `batchUpdate`: UpdateParagraphStyleRequest with range |
| `getLinkUrl()` | String | Gets hyperlink URL | Read `TextRun.textStyle.link.url` |
| `setLinkUrl(url)` | Text | Sets hyperlink | `batchUpdate`: UpdateTextStyleRequest with `link` |
| `getLinkUrl(offset)` | String | Gets link at offset | Read `TextRun.textStyle.link` at position |
| `setLinkUrl(startOffset, endOffsetInclusive, url)` | Text | Sets link for range | `batchUpdate`: UpdateTextStyleRequest with range |
| **Attributes** |
| `getAttributes()` | Object | Gets all attributes | Read entire `TextRun.textStyle` |
| `setAttributes(attributes)` | Text | Applies attribute map | `batchUpdate`: UpdateTextStyleRequest with multiple fields |
| `getAttributes(offset)` | Object | Gets attributes at offset | Read `TextRun.textStyle` at position |
| `setAttributes(startOffset, endOffsetInclusive, attributes)` | Text | Applies attributes to range | `batchUpdate`: UpdateTextStyleRequest with range |
| **Search & Replace** |
| `findText(searchPattern)` | RangeElement | Locates text via regex | Client-side search through `TextRun.content` |
| `findText(searchPattern, from)` | RangeElement | Continues search | Client-side search with offset |
| `replaceText(searchPattern, replacement)` | Element | Find-and-replace | `batchUpdate`: ReplaceAllTextRequest |
| **Navigation** |
| `getParent()` | ContainerElement | Gets parent | Navigate document structure |
| `getNextSibling()` | Element | Gets next sibling | Navigate `ParagraphElement` array |
| `getPreviousSibling()` | Element | Gets previous sibling | Navigate `ParagraphElement` array |
| `getType()` | ElementType | Returns element type | Check `ParagraphElement` union field |
| `isAtDocumentEnd()` | Boolean | Checks if at end | Compare `endIndex` to document length |
| **Structural** |
| `copy()` | Text | Creates detached copy | Read and reconstruct via API |
| `merge()` | Text | Merges with previous sibling | `batchUpdate`: DeleteContentRangeRequest to merge runs |
| `removeFromParent()` | Text | Removes element | `batchUpdate`: DeleteContentRangeRequest |

### Key Differences from REST API

**Apps Script Text class:**
- **Mutable wrapper**: Text is an object with methods that modify the document
- **Fluent API**: Most methods return `Text` for chaining (e.g., `text.setBold(true).setFontSize(14)`)
- **Character-level precision**: Every formatting method has variants for entire text, single offset, or range
- **Direct attribute maps**: `setAttributes()` accepts key-value objects matching DocumentApp.Attribute enums
- **Integrated search**: `findText()` and `replaceText()` built into the Text class

**REST API TextRun:**
- **Read-only structure**: TextRun is a data object in API responses, not a mutable object
- **Batch mutations**: All modifications go through `batchUpdate` with request objects
- **Field masks required**: UpdateTextStyleRequest requires explicit field masks to specify which properties to update
- **Index-based operations**: InsertTextRequest, UpdateTextStyleRequest use absolute document indexes
- **No built-in search**: Must fetch document, search client-side, then send batch updates

---

## InlineImage

An embedded image within a paragraph or list item.

### Characteristics

- Cannot be placed in FootnoteSection
- Cannot contain other elements (leaf node)
- Represents images inline with text flow

### Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `getAltDescription()` | String | Gets alt description | Read `InlineObject.inlineObjectProperties.embeddedObject.description` |
| `setAltDescription(description)` | InlineImage | Sets alt description | `batchUpdate`: UpdateInlineObjectPropertiesRequest with `description` |
| `getAltTitle()` | String | Gets alt title | Read `InlineObject.inlineObjectProperties.embeddedObject.title` |
| `setAltTitle(title)` | InlineImage | Sets alt title | `batchUpdate`: UpdateInlineObjectPropertiesRequest with `title` |
| `getHeight()` | Integer | Gets height in pixels | Read `InlineObject.inlineObjectProperties.embeddedObject.size.height` |
| `setHeight(height)` | InlineImage | Sets height | `batchUpdate`: UpdateInlineObjectPropertiesRequest with `size.height` |
| `getWidth()` | Integer | Gets width in pixels | Read `InlineObject.inlineObjectProperties.embeddedObject.size.width` |
| `setWidth(width)` | InlineImage | Sets width | `batchUpdate`: UpdateInlineObjectPropertiesRequest with `size.width` |
| `getLinkUrl()` | String | Gets hyperlink URL | Read `TextRun.textStyle.link.url` (for containing TextRun) |
| `setLinkUrl(url)` | InlineImage | Sets hyperlink | `batchUpdate`: UpdateTextStyleRequest on InlineObjectElement's TextStyle |
| `getAs(contentType)` | Blob | Converts image to MIME type | Fetch `ImageProperties.contentUri` and convert |
| `getBlob()` | Blob | Gets image data | Fetch from `ImageProperties.contentUri` |
| `getAttributes()` | Object | Gets element attributes | Read `InlineObject.inlineObjectProperties.embeddedObject` |
| `setAttributes(attributes)` | InlineImage | Sets attributes | `batchUpdate`: UpdateInlineObjectPropertiesRequest |
| `copy()` | InlineImage | Creates detached copy | Read and reconstruct |
| `merge()` | InlineImage | Merges with previous sibling | Not directly supported |
| `removeFromParent()` | InlineImage | Removes element | `batchUpdate`: DeleteContentRangeRequest |
| `getNextSibling()` | Element | Gets next sibling | Navigate `ParagraphElement` array |
| `getPreviousSibling()` | Element | Gets previous sibling | Navigate `ParagraphElement` array |
| `getParent()` | ContainerElement | Gets parent | Navigate document structure |
| `getType()` | ElementType | Returns INLINE_IMAGE | Check `ParagraphElement.inlineObjectElement` |
| `isAtDocumentEnd()` | Boolean | Checks if at end | Compare `endIndex` to document length |

### Key Differences from REST API

**Apps Script InlineImage:**
- Direct image manipulation (get/set dimensions, alt text)
- Blob access methods for image data
- Link URL management built into the class

**REST API InlineObjectElement:**
- References an `inlineObjectId` that maps to `Document.inlineObjects[id]`
- Image data accessed via `EmbeddedObject.imageProperties.contentUri`
- Dimensions stored in `EmbeddedObject.size` as `Dimension` objects with `magnitude` and `unit`
- Alt text stored in `EmbeddedObject.title` and `description`
- Links stored in `TextRun.textStyle.link`, not on the InlineObject itself

---

## PositionedImage

A fixed-position image anchored to a paragraph.

### Characteristics

- Not a document element (lacks parent/sibling relationships)
- Anchored to specific paragraph/list item
- Positioned using point-based offsets
- Each has a unique ID

### Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `getId()` | String | Gets unique identifier | Read `PositionedObject.objectId` |
| `getHeight()` | Integer | Gets height in pixels | Read `PositionedObject.positionedObjectProperties.embeddedObject.size.height` |
| `setHeight(height)` | PositionedImage | Sets height | `batchUpdate`: UpdatePositionedObjectPropertiesRequest |
| `getWidth()` | Integer | Gets width in pixels | Read `PositionedObject.positionedObjectProperties.embeddedObject.size.width` |
| `setWidth(width)` | PositionedImage | Sets width | `batchUpdate`: UpdatePositionedObjectPropertiesRequest |
| `getLayout()` | PositionedLayout | Gets layout mode | Read `PositionedObject.positionedObjectProperties.positioning.layout` |
| `setLayout(layout)` | PositionedImage | Sets layout mode | `batchUpdate`: UpdatePositionedObjectPropertiesRequest |
| `getLeftOffset()` | Number | Gets left offset (points) | Read `PositionedObject.positionedObjectProperties.positioning.leftOffset` |
| `setLeftOffset(offset)` | PositionedImage | Sets left offset | `batchUpdate`: UpdatePositionedObjectPropertiesRequest |
| `getTopOffset()` | Number | Gets top offset (points) | Read `PositionedObject.positionedObjectProperties.positioning.topOffset` |
| `setTopOffset(offset)` | PositionedImage | Sets top offset | `batchUpdate`: UpdatePositionedObjectPropertiesRequest |
| `getParagraph()` | Paragraph | Gets anchor paragraph | Find paragraph containing the positioned object reference |
| `getAs(contentType)` | Blob | Converts image to MIME type | Fetch `ImageProperties.contentUri` and convert |
| `getBlob()` | Blob | Gets image data | Fetch from `ImageProperties.contentUri` |

### Key Differences from REST API

**Apps Script PositionedImage:**
- Direct access to anchor paragraph via `getParagraph()`
- Layout enum is simpler (PositionedLayout)
- Offset units are always points

**REST API PositionedObject:**
- Stored in `Document.positionedObjects` dictionary
- No direct back-reference to anchor paragraph (must search document structure)
- Layout stored as `PositionedObjectLayout` enum (WRAP_TEXT, BREAK_LEFT, BREAK_RIGHT, etc.)
- Offsets are `Dimension` objects with explicit `unit` field

---

## InlineDrawing

An embedded drawing within a paragraph or list item.

### Characteristics

- Cannot be in FootnoteSection
- Cannot contain other elements (leaf node)
- Represents Google Drawings embedded inline

### Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `getAltDescription()` | String | Gets alt description | Read `InlineObject.inlineObjectProperties.embeddedObject.description` |
| `setAltDescription(description)` | InlineDrawing | Sets alt description | `batchUpdate`: UpdateInlineObjectPropertiesRequest |
| `getAltTitle()` | String | Gets alt title | Read `InlineObject.inlineObjectProperties.embeddedObject.title` |
| `setAltTitle(title)` | InlineDrawing | Sets alt title | `batchUpdate`: UpdateInlineObjectPropertiesRequest |
| `getAttributes()` | Object | Gets element attributes | Read `InlineObject.inlineObjectProperties.embeddedObject` |
| `setAttributes(attributes)` | InlineDrawing | Sets attributes | `batchUpdate`: UpdateInlineObjectPropertiesRequest |
| `copy()` | InlineDrawing | Creates detached copy | Read and reconstruct |
| `merge()` | InlineDrawing | Merges with previous sibling | Not directly supported |
| `removeFromParent()` | InlineDrawing | Removes element | `batchUpdate`: DeleteContentRangeRequest |
| `getNextSibling()` | Element | Gets next sibling | Navigate `ParagraphElement` array |
| `getPreviousSibling()` | Element | Gets previous sibling | Navigate `ParagraphElement` array |
| `getParent()` | ContainerElement | Gets parent | Navigate document structure |
| `getType()` | ElementType | Returns INLINE_DRAWING | Check `ParagraphElement.inlineObjectElement` |
| `isAtDocumentEnd()` | Boolean | Checks if at end | Compare `endIndex` to document length |

### Key Differences from REST API

**Apps Script InlineDrawing:**
- Dedicated class for drawings (distinct from images)
- No dimension methods (drawings have intrinsic sizes)

**REST API InlineObject:**
- No distinction between images and drawings at the element level
- Both use `InlineObjectElement` referencing `Document.inlineObjects`
- Drawing content identified by `EmbeddedObject.embeddedDrawingProperties` (currently empty object)
- Dimensions still stored in `EmbeddedObject.size`

---

## HorizontalRule

A horizontal divider line.

### Characteristics

- Cannot contain other elements (leaf node)
- Can be in Paragraph or ListItem
- Renders as visual separator

### Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `getAttributes()` | Object | Gets element attributes | Read `HorizontalRule` object |
| `setAttributes(attributes)` | HorizontalRule | Sets attributes | `batchUpdate`: UpdateTextStyleRequest (inherited style) |
| `copy()` | HorizontalRule | Creates detached copy | Read and reconstruct |
| `removeFromParent()` | HorizontalRule | Removes element | `batchUpdate`: DeleteContentRangeRequest |
| `getNextSibling()` | Element | Gets next sibling | Navigate `ParagraphElement` array |
| `getPreviousSibling()` | Element | Gets previous sibling | Navigate `ParagraphElement` array |
| `getParent()` | ContainerElement | Gets parent | Navigate document structure |
| `getType()` | ElementType | Returns HORIZONTAL_RULE | Check `ParagraphElement.horizontalRule` |
| `isAtDocumentEnd()` | Boolean | Checks if at end | Compare `endIndex` to document length |

### Key Differences from REST API

**Apps Script HorizontalRule:**
- Dedicated class with attribute management
- Can set visual attributes directly

**REST API HorizontalRule:**
- Simple object in `ParagraphElement.horizontalRule`
- Only contains `textStyle` (inherited formatting) and suggestion tracking
- No configuration properties (horizontal rules are just visual dividers)

---

## PageBreak

Forces content to continue on next page.

### Characteristics

- Cannot be in Table, HeaderSection, FooterSection, or FootnoteSection
- Can be in Paragraph or ListItem
- Forces page boundary

### Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `getAttributes()` | Object | Gets element attributes | Read `PageBreak` object |
| `setAttributes(attributes)` | PageBreak | Sets attributes | `batchUpdate`: UpdateTextStyleRequest (inherited style) |
| `copy()` | PageBreak | Creates detached copy | Read and reconstruct |
| `removeFromParent()` | PageBreak | Removes element | `batchUpdate`: DeleteContentRangeRequest |
| `getNextSibling()` | Element | Gets next sibling | Navigate `ParagraphElement` array |
| `getPreviousSibling()` | Element | Gets previous sibling | Navigate `ParagraphElement` array |
| `getParent()` | ContainerElement | Gets parent | Navigate document structure |
| `getType()` | ElementType | Returns PAGE_BREAK | Check `ParagraphElement.pageBreak` |
| `isAtDocumentEnd()` | Boolean | Checks if at end | Compare `endIndex` to document length |

### Key Differences from REST API

**Apps Script PageBreak:**
- Dedicated class with methods
- Can manipulate placement constraints

**REST API PageBreak:**
- Simple object in `ParagraphElement.pageBreak`
- Only contains `textStyle` (inherited formatting) and suggestion tracking
- No configuration properties beyond inherited styles

---

## Coverage Summary

### Documented Classes

| Apps Script Class | REST API Equivalent | Completeness |
|-------------------|---------------------|--------------|
| Text | TextRun | ✅ Full coverage |
| InlineImage | InlineObjectElement → InlineObject (image) | ✅ Full coverage |
| PositionedImage | PositionedObject (image) | ✅ Full coverage |
| InlineDrawing | InlineObjectElement → InlineObject (drawing) | ✅ Full coverage |
| HorizontalRule | ParagraphElement.horizontalRule | ✅ Full coverage |
| PageBreak | ParagraphElement.pageBreak | ✅ Full coverage |

### REST API Elements Without Apps Script Equivalents

| REST API Element | Description | Why No Apps Script Class |
|------------------|-------------|--------------------------|
| Person | @-mention smart chips | Added after Apps Script core API |
| RichLink | Smart chip links to Google resources | Added after Apps Script core API |
| DateElement | Smart date chips with locale-specific rendering | Added after Apps Script core API |
| AutoText | Auto-generated text (page numbers, page count) | Handled via different Apps Script mechanisms |
| ColumnBreak | Forces content to next column | Apps Script may use different approach |
| FootnoteReference | Reference to footnote | Likely handled by Footnote class methods |
| Equation | Mathematical equations | Equation class exists in Apps Script |

### Apps Script Advantages

1. **Fluent API**: Method chaining for text formatting
2. **Character-level precision**: Range-based operations built into every formatting method
3. **Direct blob access**: `getBlob()` and `getAs()` for images
4. **Integrated search**: `findText()` and `replaceText()` built into Text class
5. **Simpler mental model**: Objects are mutable wrappers, not read-only structures

### REST API Advantages

1. **Modern smart chips**: Person, RichLink, DateElement support
2. **Batch efficiency**: Single `batchUpdate` for multiple operations
3. **Explicit field masks**: Fine-grained control over what changes
4. **Suggestion tracking**: Built into every element type
5. **Language-agnostic**: HTTP API works from any platform
