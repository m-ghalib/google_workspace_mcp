# Smart Chips (Person, Date, RichLink)

Smart chips are inline elements in Google Docs that represent structured data like people, dates, and links to Google resources. All three smart chip types are **read-only in both Apps Script and the REST API** — they can only be inserted through the Google Docs UI, but both APIs can detect and read their properties.

**Key difference from REST API**: While both APIs are read-only for smart chips, Apps Script provides convenient accessor methods (e.g., `getName()`, `getEmail()`, `getUrl()`) while the REST API requires parsing nested property objects. Both APIs can read the same underlying data.

## Person

Represents a link to a person, identified by an email address. Optionally includes a display name, which appears in the document instead of the email when set.

### Methods

| Method | Return Type | Description |
|--------|------------|-------------|
| `copy()` | Person | Creates a detached, deep copy of the element |
| `getAttributes()` | Object | Retrieves the element's attributes |
| `getEmail()` | String | Returns the person's email address |
| `getName()` | String \| null | Returns the display name if set, or null if displaying email |
| `getNextSibling()` | Element \| null | Retrieves the next sibling element |
| `getParent()` | ContainerElement \| null | Retrieves the parent element |
| `getPreviousSibling()` | Element \| null | Retrieves the previous sibling element |
| `getType()` | ElementType | Retrieves the element's type |
| `isAtDocumentEnd()` | Boolean | Determines if element is at document end |
| `merge()` | Person \| null | Merges with preceding sibling of same type |
| `removeFromParent()` | Person \| null | Removes element from its parent |
| `setAttributes(attributes)` | Person | Sets the element's attributes |

### REST API Comparison

**REST API Person structure**:
- `personId` - unique identifier
- `personProperties` - object containing `name` and `email`
- `textStyle` - formatting applied to the chip
- `suggestedInsertionIds[]`, `suggestedDeletionIds[]` - suggestion tracking
- Occupies exactly 1 character position (startIndex to endIndex span of 1)

**Apps Script advantages**:
- Direct accessor methods: `getEmail()` and `getName()` vs. parsing nested `personProperties`
- Inherits element navigation methods from parent class
- Same read-only limitations as REST API — neither can insert new Person chips

## Date

Represents a formatted date element with configurable display text, locale, and timestamp. The Date chip can render in different formats while preserving the underlying timestamp value.

### Methods

| Method | Return Type | Description |
|--------|-------------|-------------|
| `copy()` | Date | Creates a detached deep copy with child elements |
| `getAttributes()` | Object | Retrieves element attributes |
| `getDisplayText()` | String | Returns the rendered display value shown in the document |
| `getLocale()` | String | Returns the date's locale (e.g., "en") |
| `getNextSibling()` | Element \| null | Retrieves next sibling element |
| `getParent()` | ContainerElement \| null | Retrieves parent element |
| `getPreviousSibling()` | Element \| null | Retrieves previous sibling element |
| `getTimestamp()` | Date | Returns the associated timestamp |
| `getType()` | ElementType | Determines element's type |
| `isAtDocumentEnd()` | Boolean | Checks if element is at document end |
| `merge()` | Date \| null | Merges with preceding sibling of same type |
| `removeFromParent()` | Date \| null | Removes element from parent |
| `setAttributes(attributes)` | Date | Sets element's attributes |

### REST API Comparison

**REST API Date structure** (called `DateElement`):
- `dateId` - unique identifier
- `dateElementProperties` - object containing:
  - `timestamp` - ISO 8601 timestamp
  - `locale` - BCP 47 language code
  - `dateFormat` - format for date portion
  - `timeFormat` - format for time portion
  - `displayText` - rendered display value
- `textStyle` - formatting applied to the chip
- `suggestedInsertionIds[]`, `suggestedDeletionIds[]` - suggestion tracking
- Occupies exactly 1 character position

**Apps Script advantages**:
- `getDisplayText()` directly returns the formatted display value
- `getTimestamp()` returns a native JavaScript Date object vs. parsing ISO 8601 string
- `getLocale()` extracts locale without navigating nested properties
- Same read-only limitations as REST API

## RichLink

Represents a link to a Google resource, such as a Drive file or YouTube video. The chip displays a title and can include a MIME type for Drive files.

### Methods

| Method | Return Type | Description |
|--------|------------|-------------|
| `copy()` | RichLink | Creates a detached, deep copy of the element |
| `getAttributes()` | Object | Retrieves the element's attributes |
| `getMimeType()` | String \| null | Returns MIME type for Drive file links; null otherwise |
| `getNextSibling()` | Element \| null | Retrieves the next sibling element |
| `getParent()` | ContainerElement \| null | Retrieves the parent element |
| `getPreviousSibling()` | Element \| null | Retrieves the previous sibling element |
| `getTitle()` | String | Returns the link's displayed title |
| `getType()` | ElementType | Retrieves the element type |
| `getUrl()` | String | Returns the resource URL |
| `isAtDocumentEnd()` | Boolean | Checks if element is at document end |
| `merge()` | RichLink \| null | Merges with preceding sibling of same type |
| `removeFromParent()` | RichLink \| null | Removes element from parent |
| `setAttributes(attributes)` | RichLink | Sets the element's attributes |

### REST API Comparison

**REST API RichLink structure**:
- `richLinkId` - unique identifier
- `richLinkProperties` - object containing:
  - `title` - displayed title
  - `uri` - target URL
  - `mimeType` - MIME type (for Drive files)
- `textStyle` - formatting applied to the chip
- `suggestedInsertionIds[]`, `suggestedDeletionIds[]` - suggestion tracking
- Occupies exactly 1 character position

**Apps Script advantages**:
- Direct accessor methods: `getTitle()`, `getUrl()`, `getMimeType()` vs. parsing `richLinkProperties`
- Inherits element navigation methods from parent class
- Same read-only limitations as REST API

## Summary Comparison

| Feature | Apps Script | REST API |
|---------|-------------|----------|
| **Insert new chips** | No | No |
| **Read chip properties** | Yes, via accessor methods | Yes, via nested property objects |
| **Data access** | Direct methods (`getEmail()`, `getUrl()`, `getDisplayText()`) | Parse nested structures (`personProperties.email`) |
| **Character position** | Implicit via element hierarchy | Explicit via `startIndex`/`endIndex` (always 1 character) |
| **Suggestion tracking** | Not exposed | Full access via `suggestedInsertionIds[]`, `suggestedDeletionIds[]` |
| **Navigation** | Inherited methods (`getNextSibling()`, `getParent()`) | Manual index-based traversal |
| **Use case** | Script-based automation, reading metadata | Batch operations, precise index control |

**When to use Apps Script**: When you need to traverse a document and extract structured data from smart chips (e.g., collecting all email addresses from Person chips, or extracting timestamps from Date chips).

**When to use REST API**: When you need suggestion tracking, precise character positioning, or batch operations across multiple chips.
