# Tabs and Table of Contents

This document covers the Apps Script classes for working with document tabs and tables of contents: **Tab**, **DocumentTab**, and **TableOfContents**.

## Overview: Apps Script vs REST API

The tab system in Apps Script provides READ access to tab metadata and content traversal, plus UI state control (active tab). The REST API provides more comprehensive tab CRUD operations:

- **Apps Script strengths**: `getActiveTab()`, `setActiveTab()` for UI state (REST API cannot do this), DOM-like content traversal
- **REST API strengths**: `CreateTabRequest`, `DeleteTabRequest` for programmatic tab creation/deletion (Apps Script CANNOT create or delete tabs)
- **Content access**: Both provide tab content access, but Apps Script uses method-based traversal while REST API returns flat JSON structure

## Tab

Represents a tab within a Google Docs document. Provides methods to access tab contents, retrieve nested child tabs, and obtain tab metadata.

### Methods

| Method | Return Type | Description |
|--------|-------------|-------------|
| `asDocumentTab()` | DocumentTab | Retrieves the tab contents as a DocumentTab |
| `getChildTabs()` | Tab[] | Retrieves the child tabs nested within this tab |
| `getId()` | String | Retrieves the ID of the tab |
| `getIndex()` | Integer | Retrieves the 0-based index of the tab within the parent |
| `getTitle()` | String | Retrieves the title of the tab |
| `getType()` | TabType | Retrieves the type of tab |

### Usage Notes

- Use `getType()` to determine tab content type before casting with `asDocumentTab()`
- Tabs can be retrieved either individually by ID (`Document.getTab(tabId)`) or as a collection (`Document.getTabs()`)
- All methods require authorization: `https://www.googleapis.com/auth/documents` or `https://www.googleapis.com/auth/documents.currentonly`

### REST API Comparison

**Apps Script Tab:**
- 6 methods, all read-only
- Provides `getChildTabs()` for hierarchical traversal
- No tab creation or deletion

**REST API Tab:**
- Fields: `tabProperties` (TabProperties), `childTabs[]` (Tab), `documentTab` (DocumentTab)
- TabProperties has: `tabId`, `title`, `parentTabId`, `index`, `nestingLevel`, `iconEmoji`
- Operations: `CreateTabRequest`, `DeleteTabRequest` (NOT available in Apps Script)

## DocumentTab

Represents a rich text container within a Google Document, capable of holding elements such as tables, lists, paragraphs, and other content.

### Methods

| Method | Return Type | Description |
|--------|-------------|-------------|
| `getBody()` | Body | Retrieves the tab's main content section |
| `addHeader()` | HeaderSection | Adds a tab header section if none exists |
| `addFooter()` | FooterSection | Adds a tab footer section if none exists |
| `getHeader()` | HeaderSection | Retrieves existing header section (null if none exists) |
| `getFooter()` | FooterSection | Retrieves existing footer section (null if none exists) |
| `addBookmark(position)` | Bookmark | Adds a bookmark at specified position |
| `getBookmark(id)` | Bookmark | Retrieves bookmark by ID (null if not found) |
| `getBookmarks()` | Bookmark[] | Gets all bookmarks in tab |
| `addNamedRange(name, range)` | NamedRange | Creates named range with ID for retrieval |
| `getNamedRanges()` | NamedRange[] | Gets all named ranges in tab |
| `getNamedRanges(name)` | NamedRange[] | Gets named ranges matching name |
| `getNamedRangeById(id)` | NamedRange | Gets named range by ID (null if not found) |
| `newPosition(element, offset)` | Position | Creates location reference within tab |
| `newRange()` | RangeBuilder | Constructs Range objects from elements |
| `getFootnotes()` | Footnote[] | Retrieves all footnotes in tab body (null if none) |

### Usage Notes

- Retrieve DocumentTab instances via `Document.getTabs()[tabIndex].asDocumentTab()` or `Document.getTab(tabId).asDocumentTab()`
- **Named Ranges**: Supports non-unique names across tabs but unique IDs within the document
- **Headers/Footers**: Tab-specific sections separate from body content
- **Position/Range Building**: Enables precise content manipulation through Position and RangeBuilder objects
- All methods require authorization: `https://www.googleapis.com/auth/documents` or `https://www.googleapis.com/auth/documents.currentonly`

### REST API Comparison

**Apps Script DocumentTab:**
- 15 methods for accessing and creating content structures
- Methods for creating headers/footers, bookmarks, named ranges
- DOM-like navigation through `newPosition()` and `newRange()`

**REST API DocumentTab:**
- Fields: `body`, `headers`, `footers`, `footnotes`, `documentStyle`, `namedStyles`, `lists`, `namedRanges`, `inlineObjects`, `positionedObjects`
- All content returned as flat JSON structure with index-based addressing
- No "create header" operation - headers/footers are modified via `batchUpdate` requests

## TableOfContents

Represents an element containing a table of contents in Google Docs. May contain ListItem, Paragraph, and Table elements, though contents are usually generated automatically by Google Docs.

### Methods

**Content Manipulation:**

| Method | Return Type | Description |
|--------|-------------|-------------|
| `clear()` | ContainerElement | Removes all content from the element |
| `copy()` | ContainerElement | Creates a detached deep copy |
| `editAsText()` | Text | Provides text editing access to contents |
| `replaceText(searchPattern, replacement)` | Element | Performs regex-based text replacement |

**Search Operations:**

| Method | Return Type | Description |
|--------|-------------|-------------|
| `findElement(elementType)` | RangeElement | Locates descendant elements by type |
| `findElement(elementType, from)` | RangeElement | Locates descendant elements starting from RangeElement |
| `findText(searchPattern)` | RangeElement | Searches using regular expressions |
| `findText(searchPattern, from)` | RangeElement | Searches starting from RangeElement |

**Structural Access:**

| Method | Return Type | Description |
|--------|-------------|-------------|
| `getChild(childIndex)` | Element | Retrieves child at specified position |
| `getChildIndex(child)` | Integer | Retrieves child's index position |
| `getNumChildren()` | Integer | Returns total child count |
| `getParent()` | ContainerElement | Accesses parent element |
| `getNextSibling()` | Element | Navigates to next sibling element |
| `getPreviousSibling()` | Element | Navigates to previous sibling element |
| `removeFromParent()` | TableOfContents | Detaches from parent element |

**Attribute Management:**

| Method | Return Type | Description |
|--------|-------------|-------------|
| `getAttributes()` | Object | Gets element properties |
| `setAttributes(attributes)` | TableOfContents | Sets element properties |
| `getLinkUrl()` | String | Gets hyperlink URL |
| `setLinkUrl(url)` | TableOfContents | Sets hyperlink URL |
| `getTextAlignment()` | TextAlignment | Gets text alignment |
| `setTextAlignment(textAlignment)` | TableOfContents | Sets text alignment |

**Information Retrieval:**

| Method | Return Type | Description |
|--------|-------------|-------------|
| `getText()` | String | Extracts text content |
| `getType()` | ElementType | Returns ElementType.TABLE_OF_CONTENTS |
| `isAtDocumentEnd()` | Boolean | Checks if at document terminus |

### Usage Notes

- TableOfContents extends ContainerElement, inheriting full editing and traversal methods
- Contents are usually auto-generated by Google Docs, but can be manually edited
- Can contain ListItem, Paragraph, and Table elements
- Most methods require authorization: `https://www.googleapis.com/auth/documents` or `https://www.googleapis.com/auth/documents.currentonly`

### REST API Comparison

**Apps Script TableOfContents:**
- Extends ContainerElement with ~25 methods
- Full editing capabilities: `clear()`, `replaceText()`, `editAsText()`
- Tree traversal methods: `getChild()`, `getParent()`, `findElement()`
- Treated as mutable content structure

**REST API TableOfContents:**
- Fields: `content[]` (array of StructuralElement)
- Treated as READ-ONLY structural content
- No direct editing operations - must use index-based `DeleteContentRangeRequest` / `InsertTextRequest` to modify
- Auto-generated TOCs are updated by Google Docs service, not exposed via API

## Summary Comparison: Apps Script vs REST API

| Feature | Apps Script | REST API |
|---------|-------------|----------|
| **Tab Creation** | Not supported | CreateTabRequest |
| **Tab Deletion** | Not supported | DeleteTabRequest |
| **Tab Metadata Access** | getId(), getTitle(), getIndex() | tabProperties.tabId, title, index |
| **Child Tabs** | getChildTabs() for traversal | childTabs[] array |
| **Active Tab Control** | getActiveTab(), setActiveTab() | Not supported |
| **Content Access Model** | Method-based DOM traversal | Flat JSON with index addressing |
| **DocumentTab Content** | getBody() returns Body object | documentTab.body as JSON |
| **Headers/Footers** | addHeader(), getHeader() methods | headers[], footers[] arrays |
| **Named Ranges** | addNamedRange(), getNamedRanges() | namedRanges map in JSON |
| **TableOfContents Editing** | Full ContainerElement methods | Read-only, edit via index operations |
| **TOC Generation** | Auto-generated by Google Docs | Auto-generated by Google Docs |

**Key Takeaway**: Apps Script provides UI-friendly read/edit access with DOM-like traversal, while REST API offers comprehensive CRUD with declarative batch operations and index-based addressing.
