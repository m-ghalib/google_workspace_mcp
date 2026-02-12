# ContainerElement (Abstract Base Class)

This document covers the **ContainerElement** abstract base class, which is the foundation for all elements in Google Apps Script that can contain other elements.

## Overview

ContainerElement is the core abstraction that gives Apps Script its DOM-like tree traversal model. It defines a shared set of ~36 methods available on ALL container types in Google Docs. This unified interface enables consistent content manipulation, search, and navigation across different element types.

**Concrete classes that inherit from ContainerElement:**
- Body
- Paragraph
- Table
- TableRow
- TableCell
- ListItem
- HeaderSection
- FooterSection
- FootnoteSection
- TableOfContents
- Equation

Every method documented below is available on all these concrete types.

## REST API Comparison

The REST API has NO equivalent abstract base class. This is a fundamental architectural difference:

- **Apps Script approach**: Unified ContainerElement interface provides consistent methods across all container types. Tree traversal via `getChild()`, `getParent()`, `findElement()`, `findText()`.
- **REST API approach**: Each structural element type has its own flat schema. No shared interface. Content addressed by absolute index positions, not tree navigation.

The ContainerElement abstraction is what makes Apps Script feel "DOM-like" compared to the REST API's declarative, index-based model.

## Methods

### Type Conversion Methods (11 methods)

These methods cast the container to specific concrete types. Use after checking `getType()` to determine the actual element type.

| Method | Return Type | Description |
|--------|-------------|-------------|
| `asBody()` | Body | Returns the element as a Body |
| `asEquation()` | Equation | Returns the element as an Equation |
| `asFooterSection()` | FooterSection | Returns the element as a FooterSection |
| `asFootnoteSection()` | FootnoteSection | Returns the element as a FootnoteSection |
| `asHeaderSection()` | HeaderSection | Returns the element as a HeaderSection |
| `asListItem()` | ListItem | Returns the element as a ListItem |
| `asParagraph()` | Paragraph | Returns the element as a Paragraph |
| `asTable()` | Table | Returns the element as a Table |
| `asTableCell()` | TableCell | Returns the element as a TableCell |
| `asTableOfContents()` | TableOfContents | Returns the element as a TableOfContents |
| `asTableRow()` | TableRow | Returns the element as a TableRow |

### Content Manipulation Methods (4 methods)

| Method | Return Type | Description |
|--------|-------------|-------------|
| `clear()` | ContainerElement | Removes all contents from the element |
| `copy()` | ContainerElement | Creates a detached deep copy of the element |
| `editAsText()` | Text | Obtains a Text version of the element for editing |
| `replaceText(searchPattern, replacement)` | Element | Performs regex-based text replacement |

### Search Methods (4 methods)

| Method | Return Type | Description |
|--------|-------------|-------------|
| `findElement(elementType)` | RangeElement | Locates descendant elements by type |
| `findElement(elementType, from)` | RangeElement | Locates descendant elements starting from RangeElement |
| `findText(searchPattern)` | RangeElement | Searches text using regular expressions |
| `findText(searchPattern, from)` | RangeElement | Searches text starting from RangeElement |

### Child Management Methods (3 methods)

| Method | Return Type | Description |
|--------|-------------|-------------|
| `getChild(childIndex)` | Element | Retrieves specific child element at index |
| `getChildIndex(child)` | Integer | Gets the index position of a child element |
| `getNumChildren()` | Integer | Returns the total number of child elements |

### Navigation Methods (3 methods)

| Method | Return Type | Description |
|--------|-------------|-------------|
| `getNextSibling()` | Element | Returns the next sibling element |
| `getPreviousSibling()` | Element | Returns the previous sibling element |
| `getParent()` | ContainerElement | Returns the parent container element |

### Property Access Methods (5 methods)

| Method | Return Type | Description |
|--------|-------------|-------------|
| `getAttributes()` | Object | Gets all element properties as key-value pairs |
| `getText()` | String | Extracts text content from element and descendants |
| `getType()` | ElementType | Returns the element's ElementType enum value |
| `getLinkUrl()` | String | Gets the hyperlink URL (if element is linked) |
| `getTextAlignment()` | TextAlignment | Gets the text alignment setting |

### Property Modification Methods (4 methods)

| Method | Return Type | Description |
|--------|-------------|-------------|
| `setAttributes(attributes)` | ContainerElement | Sets element properties from key-value pairs |
| `setLinkUrl(url)` | ContainerElement | Sets a hyperlink URL on the element |
| `setTextAlignment(textAlignment)` | ContainerElement | Sets the text alignment |
| `merge()` | ContainerElement | Merges element with preceding sibling of same type |

### Structural Methods (2 methods)

| Method | Return Type | Description |
|--------|-------------|-------------|
| `removeFromParent()` | ContainerElement | Detaches element from its parent |
| `isAtDocumentEnd()` | Boolean | Checks if element is at the end of the document |

## Key Capabilities Enabled by ContainerElement

### 1. Tree Traversal (No REST API Equivalent)

```javascript
// Navigate down the tree
var body = DocumentApp.getActiveDocument().getBody();
var firstChild = body.getChild(0);
var secondChild = body.getChild(1);

// Navigate up the tree
var parent = firstChild.getParent();

// Navigate horizontally
var nextSibling = firstChild.getNextSibling();
var prevSibling = secondChild.getPreviousSibling();
```

The REST API uses flat index-based addressing instead. There is no "navigate to parent" or "get next sibling" concept - you must calculate positions from the root document structure.

### 2. Recursive Search

```javascript
// Find all tables in the document
var searchResult = body.findElement(DocumentApp.ElementType.TABLE);
while (searchResult) {
  var table = searchResult.getElement().asTable();
  // Process table...
  searchResult = body.findElement(DocumentApp.ElementType.TABLE, searchResult);
}

// Find text matching a pattern
var foundText = body.findText("pattern.*here");
```

The REST API has no search functionality - you must iterate through the entire document structure yourself and match patterns manually.

### 3. Uniform Editing Interface

Because all container types inherit from ContainerElement, you can write generic code that works across different element types:

```javascript
function clearElement(container) {
  container.clear();  // Works on Body, Paragraph, TableCell, etc.
}

function findTablesIn(container) {
  return container.findElement(DocumentApp.ElementType.TABLE);
  // Works on any ContainerElement subclass
}
```

The REST API requires different request types for different operations - there is no shared interface.

## Authorization Requirements

Most ContainerElement methods require authorization with one of these scopes:
- `https://www.googleapis.com/auth/documents`
- `https://www.googleapis.com/auth/documents.currentonly`

## Summary: ContainerElement vs REST API

| Feature | ContainerElement (Apps Script) | REST API |
|---------|-------------------------------|----------|
| **Abstraction** | Unified base class for all containers | No base class - each element has flat schema |
| **Tree Navigation** | getChild(), getParent(), getNextSibling() | No equivalent - index-based addressing only |
| **Search** | findElement(), findText() with regex | No search API - manual iteration required |
| **Content Editing** | clear(), replaceText(), editAsText() | DeleteContentRangeRequest, InsertTextRequest by index |
| **Type Safety** | Runtime type checking via getType() | Schema-based validation at request time |
| **Code Reusability** | Generic functions work on any container | Element-specific request builders needed |
| **Mental Model** | DOM-like tree traversal | Declarative batch updates with absolute positioning |

**Key Takeaway**: ContainerElement is the foundational abstraction that makes Apps Script feel like manipulating a DOM tree, while the REST API treats documents as flat arrays of indexed structural elements. The unified interface is Apps Script's biggest advantage for interactive editing workflows, while the REST API's declarative model is more efficient for batch operations.
