# Sections, Ranges & Bookmarks

Document sections (headers/footers/footnotes), range selection, and bookmarks for navigation.

## HeaderSection

Represents a header section in a Document. A document typically contains at most one HeaderSection. May contain ListItem, Paragraph, and Table elements.

### Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `appendHorizontalRule()` | HorizontalRule | Creates and appends a new horizontal rule within a new paragraph | `InsertHorizontalRuleRequest` |
| `appendImage(image)` | InlineImage | Creates and appends an image from blob or copies existing InlineImage | `InsertInlineImageRequest` |
| `appendListItem(listItem)` | ListItem | Appends existing list item | `InsertTextRequest` + set `bullet` in paragraph |
| `appendListItem(text)` | ListItem | Creates and appends a list item; consecutive items form one list | `InsertTextRequest` + set `bullet` in paragraph |
| `appendParagraph(paragraph)` | Paragraph | Appends existing paragraph | `InsertTextRequest` |
| `appendParagraph(text)` | Paragraph | Creates and appends a new paragraph | `InsertTextRequest` |
| `appendTable()` | Table | Creates and appends an empty table | `InsertTableRequest` |
| `appendTable(cells)` | Table | Creates and appends a table with cell data | `InsertTableRequest` + `InsertTextRequest` |
| `appendTable(table)` | Table | Copies and appends existing table | `InsertTableRequest` + multiple updates |
| `clear()` | HeaderSection | Clears all element contents | `DeleteContentRangeRequest` for entire header |
| `copy()` | HeaderSection | Returns deep copy without parent | Read + recreate with `CreateHeaderRequest` |
| `editAsText()` | Text | Gets text version for editing (ignores non-text elements) | Use `Range` with text operations |
| `findElement(elementType)` | RangeElement \| null | Searches for descendant element type | Client-side filtering of header body elements |
| `findElement(elementType, from)` | RangeElement \| null | Searches from specified RangeElement | Client-side filtering |
| `findText(searchPattern)` | RangeElement \| null | Searches using regex patterns | `ReplaceAllTextRequest` with `matchCase` or client-side |
| `findText(searchPattern, from)` | RangeElement \| null | Searches from previous result | Client-side |
| `getAttributes()` | Object | Retrieves element attributes | Read `header` from document response |
| `getChild(childIndex)` | Element | Gets child at specified index | Access `body.content[childIndex]` in header |
| `getChildIndex(child)` | Integer | Gets index of specified child | Client-side calculation from `content` array |
| `getImages()` | InlineImage[] \| null | Retrieves all contained images | Filter `inlineObjects` by header range |
| `getListItems()` | ListItem[] \| null | Retrieves all list items | Filter paragraphs with `bullet` in header range |
| `getNumChildren()` | Integer | Gets number of children | `body.content.length` in header |
| `getParagraphs()` | Paragraph[] \| null | Retrieves all paragraphs including list items | Filter `PARAGRAPH` elements in header body |
| `getParent()` | ContainerElement \| null | Gets parent element | Document root (headers have no parent) |
| `getTables()` | Table[] \| null | Retrieves all tables | Filter `TABLE` elements in header body |
| `getText()` | String | Gets element contents as text | Concatenate all `textRun.content` in header |
| `getTextAlignment()` | TextAlignment \| null | Gets text alignment setting | `paragraphStyle.alignment` for first paragraph |
| `getType()` | ElementType | Gets element type | Always `HEADER_SECTION` |
| `insertHorizontalRule(childIndex)` | HorizontalRule | Inserts horizontal rule at index | `InsertHorizontalRuleRequest` at calculated position |
| `insertImage(childIndex, image)` | InlineImage | Inserts image at specified index | `InsertInlineImageRequest` at calculated position |
| `insertListItem(childIndex, listItem)` | ListItem | Inserts list item at index | `InsertTextRequest` at calculated position |
| `insertListItem(childIndex, text)` | ListItem | Inserts new list item at index | `InsertTextRequest` at calculated position |
| `insertParagraph(childIndex, paragraph)` | Paragraph | Inserts paragraph at index | `InsertTextRequest` at calculated position |
| `insertParagraph(childIndex, text)` | Paragraph | Inserts new paragraph at index | `InsertTextRequest` at calculated position |
| `insertTable(childIndex)` | Table | Inserts empty table at index | `InsertTableRequest` at calculated position |
| `insertTable(childIndex, cells)` | Table | Inserts table with cell data at index | `InsertTableRequest` + cell updates |
| `insertTable(childIndex, table)` | Table | Copies and inserts table at index | `InsertTableRequest` + multiple updates |
| `removeChild(child)` | HeaderSection | Removes specified child | `DeleteContentRangeRequest` for child's range |
| `removeFromParent()` | HeaderSection \| null | Removes from parent | `DeleteHeaderRequest` |
| `replaceText(searchPattern, replacement)` | Element | Replaces regex matches | `ReplaceAllTextRequest` with header range filter |
| `setAttributes(attributes)` | HeaderSection | Sets element attributes | `UpdateParagraphStyleRequest` for all paragraphs |
| `setText(text)` | HeaderSection | Sets contents as plain text | `DeleteContentRangeRequest` + `InsertTextRequest` |
| `setTextAlignment(textAlignment)` | HeaderSection | Sets text alignment | `UpdateParagraphStyleRequest` with `alignment` |

**REST API Mapping:**
- Headers in REST API: Created via `CreateHeaderRequest`, deleted via `DeleteHeaderRequest`
- Accessed via `Document.headers` map keyed by header ID
- Content lives in `Header.content[]` array (same structure as body)
- Each header has a unique `headerId` used in `Paragraph.elements[].textRun.textStyle.link.heading`
- Headers can be tab-specific or document-wide

---

## FooterSection

Represents a footer section in a Document. A document typically contains at most one FooterSection. May contain ListItem, Paragraph, and Table elements.

### Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `appendHorizontalRule()` | HorizontalRule | Creates and appends a new horizontal rule | `InsertHorizontalRuleRequest` |
| `appendImage(image)` | InlineImage | Creates and appends an image from blob or InlineImage | `InsertInlineImageRequest` |
| `appendListItem(text)` | ListItem | Creates and appends a list item | `InsertTextRequest` + set `bullet` |
| `appendListItem(listItem)` | ListItem | Appends existing list item | `InsertTextRequest` + set `bullet` |
| `appendParagraph(text)` | Paragraph | Creates and appends a new paragraph | `InsertTextRequest` |
| `appendParagraph(paragraph)` | Paragraph | Appends existing paragraph | `InsertTextRequest` |
| `appendTable()` | Table | Creates and appends an empty table | `InsertTableRequest` |
| `appendTable(cells)` | Table | Creates and appends a table with cell data | `InsertTableRequest` + cell updates |
| `appendTable(table)` | Table | Copies and appends existing table | `InsertTableRequest` + multiple updates |
| `insertHorizontalRule(childIndex)` | HorizontalRule | Inserts horizontal rule at index | `InsertHorizontalRuleRequest` at position |
| `insertImage(childIndex, image)` | InlineImage | Inserts image at specified index | `InsertInlineImageRequest` at position |
| `insertListItem(childIndex, text)` | ListItem | Inserts new list item at index | `InsertTextRequest` at position |
| `insertListItem(childIndex, listItem)` | ListItem | Inserts existing list item at index | `InsertTextRequest` at position |
| `insertParagraph(childIndex, text)` | Paragraph | Inserts new paragraph at index | `InsertTextRequest` at position |
| `insertParagraph(childIndex, paragraph)` | Paragraph | Inserts existing paragraph at index | `InsertTextRequest` at position |
| `insertTable(childIndex)` | Table | Inserts empty table at index | `InsertTableRequest` at position |
| `insertTable(childIndex, cells)` | Table | Inserts table with cell data at index | `InsertTableRequest` + cell updates |
| `insertTable(childIndex, table)` | Table | Copies and inserts table at index | `InsertTableRequest` + multiple updates |
| `getText()` | String | Gets element contents as text | Concatenate all `textRun.content` in footer |
| `editAsText()` | Text | Gets text version for editing | Use `Range` with text operations |
| `getImages()` | InlineImage[] \| null | Retrieves all contained images | Filter `inlineObjects` by footer range |
| `getListItems()` | ListItem[] \| null | Retrieves all list items | Filter paragraphs with `bullet` in footer range |
| `getParagraphs()` | Paragraph[] \| null | Retrieves all paragraphs | Filter `PARAGRAPH` elements in footer body |
| `getTables()` | Table[] \| null | Retrieves all tables | Filter `TABLE` elements in footer body |
| `getChild(childIndex)` | Element | Gets child at specified index | Access `body.content[childIndex]` in footer |
| `getChildIndex(child)` | Integer | Gets index of specified child | Client-side calculation from `content` array |
| `getNumChildren()` | Integer | Gets number of children | `body.content.length` in footer |
| `getParent()` | ContainerElement \| null | Gets parent element | Document root (footers have no parent) |
| `removeChild(child)` | FooterSection | Removes specified child | `DeleteContentRangeRequest` for child's range |
| `removeFromParent()` | FooterSection \| null | Removes from parent | `DeleteFooterRequest` |
| `findElement(elementType)` | RangeElement \| null | Searches for descendant element type | Client-side filtering of footer body elements |
| `findElement(elementType, from)` | RangeElement \| null | Searches from specified RangeElement | Client-side filtering |
| `findText(searchPattern)` | RangeElement \| null | Searches using regex patterns | `ReplaceAllTextRequest` or client-side |
| `findText(searchPattern, from)` | RangeElement \| null | Searches from previous result | Client-side |
| `replaceText(searchPattern, replacement)` | Element | Replaces regex matches | `ReplaceAllTextRequest` with footer range filter |
| `getAttributes()` | Object | Retrieves element attributes | Read `footer` from document response |
| `setAttributes(attributes)` | FooterSection | Sets element attributes | `UpdateParagraphStyleRequest` for all paragraphs |
| `getTextAlignment()` | TextAlignment \| null | Gets text alignment setting | `paragraphStyle.alignment` for first paragraph |
| `setTextAlignment(textAlignment)` | FooterSection | Sets text alignment | `UpdateParagraphStyleRequest` with `alignment` |
| `setText(text)` | FooterSection | Sets contents as plain text | `DeleteContentRangeRequest` + `InsertTextRequest` |
| `clear()` | FooterSection | Empties all contents | `DeleteContentRangeRequest` for entire footer |
| `copy()` | FooterSection | Produces a detached, deep duplicate | Read + recreate with `CreateFooterRequest` |
| `getType()` | ElementType | Gets element type | Always `FOOTER_SECTION` |

**REST API Mapping:**
- Footers in REST API: Created via `CreateFooterRequest`, deleted via `DeleteFooterRequest`
- Accessed via `Document.footers` map keyed by footer ID
- Content lives in `Footer.content[]` array (same structure as body)
- Each footer has a unique `footerId`
- Footers can be tab-specific or document-wide

---

## Footnote

Represents a footnote element within a ListItem or Paragraph. The Footnote itself cannot contain any other element — it has a corresponding FootnoteSection for its contents.

### Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `copy()` | Footnote | Returns a detached, deep copy | Read + recreate with footnote in `InsertTextRequest` |
| `getAttributes()` | Object | Retrieves element attributes | Read `footnoteReference` from paragraph element |
| `getFootnoteContents()` | FootnoteSection \| null | Retrieves the contents of the footnote | Read `Document.footnotes[footnoteId]` |
| `getNextSibling()` | Element \| null | Retrieves next sibling element | Access next element in `paragraph.elements[]` |
| `getParent()` | ContainerElement \| null | Retrieves parent element | Access parent paragraph |
| `getPreviousSibling()` | Element \| null | Retrieves previous sibling element | Access previous element in `paragraph.elements[]` |
| `getType()` | ElementType | Retrieves element type | Always `FOOTNOTE` |
| `isAtDocumentEnd()` | Boolean | Determines if at the end of document | Check if `endIndex` equals document end |
| `removeFromParent()` | Footnote \| null | Removes the element from parent | `DeleteContentRangeRequest` for footnote range |
| `setAttributes(attributes)` | Footnote | Sets element attributes | `UpdateTextStyleRequest` for footnote |

**REST API Mapping:**
- Footnotes in REST API: Inline element with `footnoteReference` field
- Content stored in `Document.footnotes` map keyed by footnote ID
- Each footnote reference has a `footnoteId` pointing to the footnote content
- Footnote content is a `Footnote` object with `content[]` array (similar to body structure)
- Created implicitly when inserting text with footnote reference

---

## FootnoteSection

Represents a footnote section containing the text that corresponds to a Footnote.

### Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `appendParagraph(paragraph)` | Paragraph | Adds an existing paragraph | `InsertTextRequest` at end of footnote |
| `appendParagraph(text)` | Paragraph | Generates and adds a new paragraph | `InsertTextRequest` at end of footnote |
| `clear()` | FootnoteSection | Empties all contents | `DeleteContentRangeRequest` for entire footnote |
| `copy()` | FootnoteSection | Produces a detached, deep duplicate | Read + recreate footnote |
| `editAsText()` | Text | Obtains text version for editing | Use `Range` with text operations |
| `findElement(elementType)` | RangeElement \| null | Locates descendant of specified type | Client-side filtering of footnote body |
| `findElement(elementType, from)` | RangeElement \| null | Searches from specific RangeElement | Client-side filtering |
| `findText(searchPattern)` | RangeElement \| null | Locates text matching regex | `ReplaceAllTextRequest` or client-side |
| `findText(searchPattern, from)` | RangeElement \| null | Searches for pattern from given result | Client-side |
| `getAttributes()` | Object | Retrieves all element attributes | Read `footnotes[footnoteId]` from document |
| `getChild(childIndex)` | Element | Obtains child element at index | Access `content[childIndex]` in footnote |
| `getChildIndex(child)` | Integer | Determines child's position index | Client-side calculation from `content` array |
| `getNextSibling()` | Element \| null | Retrieves following sibling | Footnotes typically have no siblings |
| `getNumChildren()` | Integer | Counts total child elements | `content.length` in footnote |
| `getParagraphs()` | Paragraph[] \| null | Retrieves all contained paragraphs | Filter `PARAGRAPH` elements in footnote |
| `getParent()` | ContainerElement \| null | Retrieves parent element | Footnote reference element |
| `getPreviousSibling()` | Element \| null | Retrieves preceding sibling | Footnotes typically have no siblings |
| `getText()` | String | Extracts element contents as text | Concatenate all `textRun.content` in footnote |
| `getTextAlignment()` | TextAlignment \| null | Retrieves alignment type | `paragraphStyle.alignment` for first paragraph |
| `getType()` | ElementType | Determines exact element classification | Always `FOOTNOTE_SECTION` |
| `insertParagraph(childIndex, paragraph)` | Paragraph | Inserts existing paragraph at index | `InsertTextRequest` at calculated position |
| `insertParagraph(childIndex, text)` | Paragraph | Generates and inserts paragraph at index | `InsertTextRequest` at calculated position |
| `removeChild(child)` | FootnoteSection | Removes specified child | `DeleteContentRangeRequest` for child's range |
| `removeFromParent()` | FootnoteSection \| null | Removes element from parent | Delete footnote reference |
| `replaceText(searchPattern, replacement)` | Element | Substitutes text matching pattern | `ReplaceAllTextRequest` with footnote range |
| `setAttributes(attributes)` | FootnoteSection | Modifies element attributes | `UpdateParagraphStyleRequest` for paragraphs |
| `setText(text)` | FootnoteSection | Assigns plain text content | `DeleteContentRangeRequest` + `InsertTextRequest` |
| `setTextAlignment(textAlignment)` | FootnoteSection | Applies text alignment setting | `UpdateParagraphStyleRequest` with `alignment` |

**REST API Mapping:**
- FootnoteSections in REST API: Accessed via `Document.footnotes[footnoteId].content[]`
- Each footnote has a `content` array with paragraphs and other elements
- Structure mirrors the body content structure
- Footnotes are keyed by `footnoteId` from the footnote reference

---

## Range

**CRITICAL ARCHITECTURAL DIFFERENCE**: Apps Script `Range` is element-based (references elements in the document tree), while REST API `Range` is index-based (uses `startIndex`/`endIndex` integers).

Apps Script Range represents a collection of document elements selected by the user or built programmatically. This is fundamentally different from the REST API's position-based ranges.

### Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `getRangeElements()` | RangeElement[] | Gets all elements including partial Text elements | Convert to index-based `Range` objects |

**REST API Mapping:**
- **Apps Script Range**: Element-based selection surviving edits (references objects, not positions)
- **REST API Range**: Index-based selection with `startIndex`/`endIndex` in UTF-16 code units
- **Key difference**: Apps Script Ranges track elements; REST API Ranges track character positions
- REST API `Range` has `startIndex`, `endIndex`, `segmentId`, `tabId` fields
- To convert: Must calculate index positions from element positions
- Apps Script Ranges are more resilient to edits but less precise
- REST API Ranges are precise but become invalid after document changes

**Trade-offs:**
- **Apps Script (element-based)**: Survives document edits, but can't select partial words precisely
- **REST API (index-based)**: Pixel-perfect precision, but invalidated by any text changes before the range

---

## RangeBuilder

Builder class for constructing Range objects from document elements. Follows the builder pattern with method chaining.

### Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `addElement(element)` | RangeBuilder | Incorporates an entire Element | Calculate element's `startIndex`/`endIndex` |
| `addElement(textElement, startOffset, endOffsetInclusive)` | RangeBuilder | Incorporates a portion of a Text element | Add character offsets to base index |
| `addElementsBetween(startElement, endElementInclusive)` | RangeBuilder | Adds two elements and all intervening elements | Calculate range from first to last element |
| `addElementsBetween(startTextElement, startOffset, endTextElementInclusive, endOffsetInclusive)` | RangeBuilder | Adds partial text elements and all between them | Calculate range with partial offsets |
| `addRange(range)` | RangeBuilder | Merges contents of existing Range | Merge multiple `Range` objects |
| `build()` | Range | Finalizes and returns the constructed range | Return array of `Range` objects |
| `getRangeElements()` | RangeElement[] | Retrieves all elements in document order | Convert element-based to index-based ranges |

**REST API Mapping:**
- No direct RangeBuilder equivalent in REST API
- REST API builds ranges directly with `{ startIndex, endIndex, segmentId, tabId }`
- Apps Script RangeBuilder is needed because Apps Script works with element objects
- In REST API, you just specify the numeric indices directly
- RangeBuilder's element-based approach is unique to Apps Script's object model

---

## RangeElement

Wrapper around an Element with possible start and end offsets for partial Text element selections.

### Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `getElement()` | Element | Retrieves the Element | Access element object in content array |
| `getStartOffset()` | Integer | Character position marking beginning (-1 for non-Text) | `startIndex` in REST API Range |
| `getEndOffsetInclusive()` | Integer | Character position marking end (-1 for non-Text) | `endIndex - 1` in REST API Range |
| `isPartial()` | Boolean | Whether range encompasses entire element or just portion | Compare `startIndex`/`endIndex` to element bounds |

**REST API Mapping:**
- RangeElement combines element reference with character offsets
- REST API uses separate `Range` objects with just indices
- Apps Script needs RangeElement because it's element-centric
- REST API's `Range.startIndex`/`endIndex` serve similar purpose but at document level
- RangeElement offsets are relative to the element; REST API indices are absolute document positions

---

## Position

Reference to a specific cursor location in a document tab, relative to a specific element.

### Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `getElement()` | Element | Retrieves the container or Text element | Find element at index in content array |
| `getOffset()` | Integer | Gets numeric position within element | Character index for Text; child index for containers |
| `getSurroundingText()` | Text | Creates artificial Text element for paragraph/list item | Reconstruct text from paragraph elements |
| `getSurroundingTextOffset()` | Integer | Gets character index within surrounding text | Calculate relative position in paragraph |
| `insertBookmark()` | Bookmark | Creates and inserts a new bookmark | `InsertBookmarkRequest` at location |
| `insertInlineImage(image)` | InlineImage \| null | Creates and inserts an image | `InsertInlineImageRequest` at location |
| `insertText(text)` | Text \| null | Inserts text at this Position | `InsertTextRequest` at location |

**REST API Mapping:**
- Apps Script Position ≈ REST API `Location` type
- REST API `Location` has `index` (absolute), `segmentId`, `tabId` fields
- Apps Script Position is element-relative; REST API Location is absolute document position
- Position's `getOffset()` is relative to parent element
- REST API's `Location.index` is absolute UTF-16 code unit position
- Insert operations in REST API require absolute index, not element-relative position

**Conversion:**
- Apps Script: Element + offset within element
- REST API: Absolute character position in document
- To convert: Sum all character lengths before the element, then add offset

---

## Bookmark

A bookmark in a Google Document for navigation and linking.

### Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `getId()` | String | Gets unique ID within DocumentTab | `Bookmark.id` field |
| `getPosition()` | Position | Retrieves bookmark position (survives edits) | Stored position when bookmark was created |
| `remove()` | void | Deletes the bookmark | `DeleteBookmarkRequest` |

**REST API Mapping:**
- **Similarity**: Both APIs have bookmarks with unique IDs
- REST API bookmark: `Bookmark` object with `id`, `name`, `tableOfContentsRole` fields
- Apps Script stores position as element reference; REST API stores as absolute index
- REST API bookmark appears in `Document.bookmarks[]` array
- Links to bookmarks: Apps Script uses `getId()`; REST API uses `BookmarkLink` with `id` and `tabId`
- Creating bookmarks: Apps Script uses `Position.insertBookmark()`; REST API uses `InsertBookmarkRequest` with `Location`
- Both survive document edits, but Apps Script's element-based tracking may be more resilient

**Key differences:**
- Apps Script: `getPosition()` returns element-relative Position
- REST API: Bookmark only stores ID and metadata, not position
- Apps Script bookmarks track their position; REST API bookmarks are just markers
- To get REST API bookmark position: Search for bookmark in document content

---

## NamedRange

A Range with a name and ID for later retrieval. Names are not unique, but IDs are unique within the tab.

### Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `getId()` | String | Gets unique ID within tab | `NamedRange.namedRangeId` field |
| `getName()` | String | Gets name (not necessarily unique) | `NamedRange.name` field |
| `getRange()` | Range | Gets associated range of elements | `NamedRange.ranges[]` array |
| `remove()` | void | Removes NamedRange without deleting content | `DeleteNamedRangeRequest` |

**REST API Mapping:**
- **Strong similarity**: Both APIs support named ranges with very similar semantics
- REST API: `NamedRange` object with `namedRangeId`, `name`, `ranges[]` fields
- REST API stores named ranges in `Document.namedRanges` map keyed by name
- Each name can have multiple ranges (hence the `NamedRanges.namedRanges[]` array)
- Creating named ranges: Apps Script uses `DocumentTab.addNamedRange(name, range)`; REST API uses `CreateNamedRangeRequest`
- Both allow multiple ranges with same name
- Both have unique IDs per range, even when names are duplicated

**Key differences:**
- Apps Script: `getRange()` returns element-based Range
- REST API: `ranges[]` contains index-based Range objects with `startIndex`/`endIndex`
- Apps Script named ranges are immutable after creation (remove only)
- REST API supports creating/deleting but not modifying named ranges
- REST API groups ranges by name in `NamedRanges` container; Apps Script treats each individually

**CRUD Operations:**
| Operation | Apps Script | REST API |
|-----------|-------------|----------|
| Create | `documentTab.addNamedRange(name, range)` | `CreateNamedRangeRequest` |
| Read | `documentTab.getNamedRanges(name)` or `namedRange.getRange()` | Access `Document.namedRanges[name].namedRanges[]` |
| Update | ❌ (immutable) | ❌ (must delete and recreate) |
| Delete | `namedRange.remove()` | `DeleteNamedRangeRequest` with `namedRangeId` |

---

## Coverage Summary

### Headers & Footers
- **Apps Script**: `HeaderSection` and `FooterSection` classes provide full content manipulation (append, insert, remove, find, replace)
- **REST API**: `CreateHeaderRequest`, `DeleteHeaderRequest`, `CreateFooterRequest`, `DeleteFooterRequest` with content in `Header.content[]` and `Footer.content[]`
- **Coverage**: Apps Script provides richer, more convenient API; REST API is lower-level but complete

### Footnotes
- **Apps Script**: `Footnote` (reference) and `FootnoteSection` (content) classes
- **REST API**: `FootnoteReference` element and `Footnote` object in `Document.footnotes[]` map
- **Coverage**: Both APIs support footnotes with similar structure; Apps Script has more convenience methods

### Ranges
- **Apps Script**: Element-based `Range`, `RangeBuilder`, `RangeElement` — survives edits, less precise
- **REST API**: Index-based `Range` with `startIndex`/`endIndex` — precise but invalidated by edits
- **Coverage**: Fundamentally different approaches; Apps Script better for resilience, REST API better for precision

### Positioning
- **Apps Script**: Element-relative `Position` class for cursor operations
- **REST API**: Absolute `Location` type with document-level indices
- **Coverage**: Both complete but use different coordinate systems

### Bookmarks
- **Apps Script**: `Bookmark` class with position tracking
- **REST API**: `Bookmark` object with metadata only; position must be found by searching
- **Coverage**: Apps Script has more convenient position tracking; REST API is more lightweight

### Named Ranges
- **Apps Script**: `NamedRange` class with element-based ranges
- **REST API**: `NamedRange` object with index-based ranges, grouped by name
- **Coverage**: Very similar functionality; main difference is element vs. index addressing

---

## Key Architectural Insights

1. **Element vs. Index Addressing**: Apps Script uses element-based references that survive edits; REST API uses absolute character positions that are faster but fragile.

2. **Convenience vs. Control**: Apps Script provides higher-level convenience methods (e.g., `appendParagraph(text)`); REST API requires explicit request construction.

3. **Sections as First-Class Objects**: Apps Script treats headers/footers/footnotes as navigable objects with methods; REST API treats them as content segments accessed via maps.

4. **Range Resilience Trade-off**: Apps Script Ranges remain valid after edits but are less precise; REST API Ranges are precise but become invalid after any content changes.

5. **Position Coordinate Systems**: Apps Script uses element-relative offsets; REST API uses absolute UTF-16 code unit indices from document start.

6. **Bookmark Position Tracking**: Apps Script bookmarks track their position automatically; REST API bookmarks are just IDs requiring manual position lookup.
