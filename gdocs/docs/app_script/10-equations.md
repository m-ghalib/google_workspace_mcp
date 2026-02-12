# Equations

Equations in Google Docs represent mathematical expressions with full structural access in Apps Script. This is a **major advantage over the REST API**, which treats equations as opaque blobs with no internal structure access.

**Key difference from REST API**: Apps Script exposes the complete equation tree structure (functions, arguments, symbols, separators) while the REST API only exposes the outermost `textStyle` — zero access to equation content or structure. Both APIs are read-only for creating equations (must be inserted via the UI), but Apps Script provides full read access while the REST API provides nearly none.

## Equation

Represents a mathematical expression that can contain `EquationFunction`, `EquationSymbol`, and `Text` elements. Acts as a container element for the equation's structural components.

### Methods

| Method | Return Type | Description |
|--------|------------|-------------|
| `clear()` | Equation | Removes all contents from the equation |
| `copy()` | Equation | Creates a detached deep copy |
| `editAsText()` | Text | Provides text editing capabilities for the equation |
| `findElement(elementType)` | RangeElement | Locates descendant elements by type |
| `findElement(elementType, from)` | RangeElement | Locates descendant elements starting from a search result |
| `findText(searchPattern)` | RangeElement | Searches for text patterns using regex |
| `findText(searchPattern, from)` | RangeElement | Searches for text starting from a search result |
| `getAttributes()` | Object | Retrieves element attributes |
| `getChild(childIndex)` | Element | Retrieves child at specified index |
| `getChildIndex(child)` | Integer | Gets position of specific child |
| `getLinkUrl()` | String | Retrieves hyperlink URL if present |
| `getNextSibling()` | Element \| null | Retrieves next sibling element |
| `getNumChildren()` | Integer | Returns count of child elements |
| `getParent()` | ContainerElement | Retrieves parent container |
| `getPreviousSibling()` | Element \| null | Retrieves previous sibling element |
| `getText()` | String | Returns equation contents as text string |
| `getTextAlignment()` | TextAlignment | Gets text alignment |
| `getType()` | ElementType | Returns the ElementType |
| `isAtDocumentEnd()` | Boolean | Checks document position |
| `merge()` | Equation | Combines with preceding sibling of same type |
| `removeFromParent()` | Equation | Detaches from parent container |
| `replaceText(searchPattern, replacement)` | Element | Replaces text using regex |
| `setAttributes(attributes)` | Equation | Sets element styling |
| `setLinkUrl(url)` | Equation | Sets hyperlink URL |
| `setTextAlignment(textAlignment)` | Equation | Sets text positioning |

### REST API Comparison

**REST API Equation structure** (opaque):
- `textStyle` - formatting applied to the equation
- `suggestedInsertionIds[]`, `suggestedDeletionIds[]` - suggestion tracking
- **That's it** — no access to internal structure, functions, symbols, or content

**Apps Script advantages**:
- **Full tree traversal**: Can navigate through all nested functions and symbols
- **Content extraction**: `getText()` returns the entire equation as a text string
- **Search capabilities**: `findElement()` and `findText()` work within equations
- **Child access**: `getChild()`, `getNumChildren()` expose hierarchical structure
- REST API treats equations as black boxes; Apps Script exposes full internals

## EquationFunction

Represents a mathematical function within an equation. Acts as a container that can contain nested `EquationFunction`, `EquationFunctionArgumentSeparator`, `EquationSymbol`, and `Text` elements. This allows for complex nested expressions like `sqrt(x^2 + y^2)`.

### Methods

| Method | Return Type | Description |
|--------|------------|-------------|
| `clear()` | EquationFunction | Removes all contents while preserving the element |
| `copy()` | EquationFunction | Creates an independent duplicate with child elements |
| `editAsText()` | Text | Enables text-based editing of the function |
| `findElement(elementType)` | RangeElement | Locates descendant elements by type |
| `findElement(elementType, from)` | RangeElement | Locates descendant elements starting from a search result |
| `findText(searchPattern)` | RangeElement | Locates text using regex patterns |
| `findText(searchPattern, from)` | RangeElement | Locates text starting from a search result |
| `getAttributes()` | Object | Retrieves formatting attributes |
| `getChild(childIndex)` | Element | Retrieves a specific child element |
| `getChildIndex(child)` | Integer | Gets position of specific child |
| `getCode()` | String | Returns the function's code identifier (e.g., "sqrt", "sum") |
| `getLinkUrl()` | String | Retrieves hyperlink URL if present |
| `getNextSibling()` | Element \| null | Navigates to next sibling |
| `getNumChildren()` | Integer | Returns total child count |
| `getParent()` | ContainerElement | Accesses the parent container |
| `getPreviousSibling()` | Element \| null | Navigates to previous sibling |
| `getText()` | String | Extracts text contents |
| `getTextAlignment()` | TextAlignment | Retrieves alignment |
| `getType()` | ElementType | Returns the ElementType |
| `isAtDocumentEnd()` | Boolean | Checks document position |
| `merge()` | EquationFunction | Combines with preceding sibling of same type |
| `removeFromParent()` | EquationFunction | Detaches element from document |
| `replaceText(searchPattern, replacement)` | Element | Updates text matching a pattern |
| `setAttributes(attributes)` | EquationFunction | Sets formatting attributes |
| `setLinkUrl(url)` | EquationFunction | Sets hyperlink URL |
| `setTextAlignment(textAlignment)` | EquationFunction | Controls alignment |

### REST API Comparison

**Apps Script advantages**:
- **`getCode()` method**: Identifies the mathematical function (e.g., "sqrt", "frac", "sum")
- **Recursive structure**: Can contain nested EquationFunction elements for complex expressions
- **Full tree access**: Navigate through arguments and nested functions
- REST API has **zero visibility** into function types or structure

## EquationFunctionArgumentSeparator

Represents a separator between function arguments (e.g., the comma in `max(x, y)`). This is a leaf element that cannot contain children.

### Methods

| Method | Return Type | Description |
|--------|------------|-------------|
| `copy()` | EquationFunctionArgumentSeparator | Creates a detached deep copy of the element |
| `getAttributes()` | Object | Retrieves the element's attributes |
| `getNextSibling()` | Element \| null | Retrieves the next sibling element |
| `getParent()` | ContainerElement \| null | Retrieves the parent element |
| `getPreviousSibling()` | Element \| null | Retrieves the previous sibling element |
| `getType()` | ElementType | Retrieves the element's type |
| `isAtDocumentEnd()` | Boolean | Checks if at document end |
| `merge()` | EquationFunctionArgumentSeparator \| null | Merges with preceding sibling of same type |
| `removeFromParent()` | EquationFunctionArgumentSeparator \| null | Removes element from parent |
| `setAttributes(attributes)` | EquationFunctionArgumentSeparator | Sets element attributes |

### REST API Comparison

**Apps Script advantages**:
- **Explicit separator detection**: Can identify argument boundaries within functions
- **Navigation**: Use `getPreviousSibling()` and `getNextSibling()` to find arguments on either side
- REST API has **zero visibility** into function arguments or separators

## EquationSymbol

Represents an individual mathematical symbol within an equation (e.g., Greek letters, operators, special characters). This is a leaf element that cannot contain children.

### Methods

| Method | Return Type | Description |
|--------|------------|-------------|
| `copy()` | EquationSymbol | Creates a detached deep copy of the current element |
| `getAttributes()` | Object | Retrieves the element's attributes as key-value pairs |
| `getCode()` | String | Retrieves the code corresponding to the equation symbol (LaTeX/Unicode representation) |
| `getNextSibling()` | Element \| null | Returns the next sibling element at the same level |
| `getParent()` | ContainerElement \| null | Returns the parent container element |
| `getPreviousSibling()` | Element \| null | Returns the previous sibling element |
| `getType()` | ElementType | Returns the element's type designation |
| `isAtDocumentEnd()` | Boolean | Checks if element is at document end |
| `merge()` | EquationSymbol \| null | Merges with preceding sibling of same type |
| `removeFromParent()` | EquationSymbol \| null | Removes element from its parent |
| `setAttributes(attributes)` | EquationSymbol | Applies specified attributes to the element |

### REST API Comparison

**Apps Script advantages**:
- **`getCode()` method**: Returns the LaTeX/Unicode code for the symbol (e.g., "\alpha", "\pi", "\sum")
- **Symbol identification**: Can programmatically detect and extract specific mathematical symbols
- REST API has **zero visibility** into individual symbols

## Summary Comparison

| Feature | Apps Script | REST API |
|---------|-------------|----------|
| **Insert equations** | No | No |
| **Read equation structure** | **Full tree access** | **None (opaque blob)** |
| **Access function types** | Yes (`getCode()` on EquationFunction) | No |
| **Access symbols** | Yes (`getCode()` on EquationSymbol) | No |
| **Detect argument separators** | Yes (EquationFunctionArgumentSeparator) | No |
| **Navigate equation tree** | Yes (getChild, getParent, siblings) | No |
| **Extract text representation** | Yes (`getText()` on Equation) | No |
| **Search within equations** | Yes (`findElement()`, `findText()`) | No |
| **Access textStyle** | Yes (via `getAttributes()`) | Yes (only thing exposed) |
| **Suggestion tracking** | Not exposed | Yes (`suggestedInsertionIds[]`) |
| **Use case** | Analyzing equation structure, extracting formulas | Styling the equation blob |

## This Is Apps Script's Biggest Advantage

Equations are the clearest example of Apps Script's structural superiority over the REST API:

- **REST API equation**: `{ "equation": { "textStyle": {...}, "suggestedInsertionIds": [] } }` — that's the entire data model
- **Apps Script equation**: Full tree of Equation → EquationFunction → nested functions/symbols/separators, with methods to traverse, search, and extract at every level

**When to use Apps Script**: Whenever you need to read, analyze, or extract content from equations. The REST API is effectively useless for equation content.

**When to use REST API**: Only if you need to apply text styling to the equation as a whole, or track suggestions. For equation content, you must use Apps Script.
